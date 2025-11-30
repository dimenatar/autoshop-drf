import random
from random import randint
from typing import Dict, List, Tuple

from celery import shared_task
from django.db.models import Prefetch
from django.utils import timezone

import core.celery_base
import core.celery_entry_point
from autoshops.models import AutoShop
from available_cars.models import AvailableCars
from cars.models import Car
from core.configs.celery_config import CeleryConfig
from discounts.models import AutoShopPersonalDiscount, GeneralDiscount
from offers.models import AutoShopOffer
from sales.models import SupplierSale
from suppliers.models import Supplier


@shared_task
def add_discount_on_cars() -> None:
    shops = AutoShop.objects.filter(is_active=True).all()
    core.celery_base.generate_discounts(shops)


@shared_task
def delete_autoshop_task() -> None:
    shops = AutoShop.objects.all().filter(is_active=True)
    company_worth_by_autoshop: Dict[AutoShop, float] = {}

    for shop in shops:
        company_worth_by_autoshop[shop] = (
                sum([car.amount * car.price for car in shop.cars_in_stock.filter(is_active=True).all()]) + shop.balance)

    if company_worth_by_autoshop:
        bankrupt = min(company_worth_by_autoshop, key=lambda k: company_worth_by_autoshop[k])
        bankrupt.is_active = False
        bankrupt.save()

        found_offers = AutoShopOffer.objects.all().filter(autoshop=bankrupt).exclude(is_active=False)
        for offer in found_offers:
            offer.is_active = False
            offer.save()


@shared_task
def create_autoshop_task() -> None:
    create_count = core.celery_base.get_create_count(AutoShop)

    car_count = Car.objects.filter(is_active=True).count()

    if create_count == 0:
        return

    autoshops_data = core.celery_base.load_json_data('autoshops', 'autoshops.json')
    if not autoshops_data:
        return

    existing_discounts = {discount.id: discount for discount in GeneralDiscount.objects.filter(is_active=True)}

    created_count = 0
    random.shuffle(autoshops_data)

    for autoshop_data in autoshops_data[:create_count]:
        if not AutoShop.objects.filter(
                name=autoshop_data['name'],
        ).exists():
            general_discount = None
            if autoshop_data.get('general_discount_id') and autoshop_data['general_discount_id'] in existing_discounts:
                general_discount = existing_discounts[autoshop_data['general_discount_id']]

            shop = AutoShop.objects.create(
                **{k: v for k, v in autoshop_data.items() if k != 'general_discount_id'},
                general_discount=general_discount
            )

            available_cars_amount = randint(3, 10)

            available_cars = [AvailableCars.objects.create(
                car=car,
                amount=randint(10, 100),
                price=CeleryConfig.get_random_car_price()
            ) for car in Car.objects.filter(is_active=True, brand=shop.desired_brand).order_by('?')[:min(car_count, available_cars_amount)]]

            shop.cars_in_stock.set(available_cars)
            shop.save()

            created_count += 1


@shared_task
def create_offers_task() -> None:
    shops = AutoShop.objects.all().filter(is_active=True)
    for shop in shops:
        create_offer(shop)


@shared_task
def purchase_cars_by_shops_from_supplier_task() -> None:
    shop_offers = AutoShopOffer.objects.filter(is_active=True).all()
    sales = SupplierSale.objects.filter(is_active=True).all()

    for offer in shop_offers:
        shop = offer.autoshop
        suitable_suppliers = get_suitable_suppliers(shop)

        if len(suitable_suppliers) == 0:
            continue

        desired_car = pick_car_to_buy(sales, suitable_suppliers)
        best_supplier, price, discount = get_best_supplier_by_price(desired_car.car, shop, suitable_suppliers)

        if shop.balance >= price:
            buy(shop, desired_car, price)
            add_sales_history(shop, best_supplier, desired_car.car, price, discount)
            offer.is_active = False
            offer.save()


def get_suitable_suppliers(shop: AutoShop) -> Dict[Supplier, List[AvailableCars]]:
    query = Supplier.objects.filter(
        is_active=True,
        cars_in_stock__car__is_active=True,
        cars_in_stock__car__model=shop.desired_model,
        cars_in_stock__car__brand=shop.desired_brand,
        cars_in_stock__car__horsepower__gte=shop.min_horsepower,
        cars_in_stock__car__horsepower__lte=shop.max_horsepower,
        cars_in_stock__car__year__gte=shop.min_year,
        cars_in_stock__car__year__lte=shop.max_year,
    ).prefetch_related(Prefetch(
        'cars_in_stock',
        queryset=AvailableCars.objects.filter(
            is_active=True,
            car__is_active=True,
            car__model=shop.desired_model,
            car__brand=shop.desired_brand,
            car__horsepower__gte=shop.min_horsepower,
            car__horsepower__lte=shop.max_horsepower,
            car__year__gte=shop.min_year,
            car__year__lte=shop.max_year,
        )
    )).distinct()

    return {supplier: list(supplier.cars_in_stock.all()) for supplier in query}


def pick_car_to_buy(sales: List[SupplierSale], cars_by_suppliers: Dict[Supplier, List[AvailableCars]]) -> AvailableCars:
    car_to_popularity = {}
    checked_cars = set()
    for supplier, cars in cars_by_suppliers.items():
        for car in cars:
            if car not in checked_cars:
                car_to_popularity[car] = sum(1 for sale in sales if sale.car == car.car)
                checked_cars.add(car)

    if len(car_to_popularity) > 0 and random.choice(range(2)) == 1:
        return max(car_to_popularity, key=lambda k: car_to_popularity[k])

    return random.choice(list(car_to_popularity.keys()))


def get_best_supplier_by_price(desired_car: Car, shop: AutoShop, cars_by_suppliers: Dict[Supplier, List[AvailableCars]]) -> Tuple[Supplier, float, float]:
    filtered_suppliers = {}

    for supplier, available_cars in cars_by_suppliers.items():
        for available_car in available_cars:
            if available_car.car == desired_car:
                filtered_suppliers[supplier] = available_car.price

    discounts_for_autoshop = list(AutoShopPersonalDiscount.objects.filter(autoshop=shop).all())

    return core.celery_base.get_best_by_price(filtered_suppliers, discounts_for_autoshop, desired_car, shop)


def buy(shop: AutoShop, car: AvailableCars, price: float) -> None:
    shop.purchase_car(car.car, price)
    car.last_purchase_date = timezone.now()


def add_sales_history(shop: AutoShop, supplier: Supplier, car: Car, price: float, discount_percent: float) -> None:
    sale = SupplierSale.objects.create(
        car=car,
        price=price,
        discount_percent=discount_percent,
        date=timezone.now(),
        supplier=supplier,
        autoshop=shop
    )
    sale.save()
    print(f"Successful purchase: {supplier} -> {car} -> {shop} for {price}")


def create_offer(shop: AutoShop) -> AutoShopOffer | None:
    if AutoShopOffer.objects.filter(is_active=True).filter(autoshop=shop).exists():
        return None

    price = CeleryConfig.get_random_car_price()

    offer = AutoShopOffer.objects.create(
        autoshop=shop,
        desired_brand=shop.desired_brand,
        desired_model=shop.desired_model,
        min_horsepower=shop.min_horsepower,
        max_horsepower=shop.max_horsepower,
        min_year=shop.min_year,
        max_year=shop.max_year,
        max_price=min(price, shop.balance),
    )

    offer.save()
    return offer
