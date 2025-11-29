import random
from datetime import datetime
from random import randint
from typing import Dict, Tuple, List
from celery import shared_task

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
    core.celery_entry_point.generate_discounts(shops)


@shared_task
def delete_autoshop_task() -> None:
    shops = AutoShop.objects.all().filter(is_active=True)
    company_worth_by_autoshop = {}

    for shop in shops:
        company_worth_by_autoshop[shop] = (
                sum([car.amount * car.price for car in shop.cars_in_stock.filter(is_active=True).all()]) + shop.balance)

    if company_worth_by_autoshop:
        bankrupt = min(company_worth_by_autoshop, key=company_worth_by_autoshop.get)
        bankrupt.is_active = False
        bankrupt.save()

        found_offers = AutoShopOffer.objects.all().filter(autoshop=bankrupt).exclude(is_active=False)
        for offer in found_offers:
            offer.is_active = False
            offer.save()


@shared_task
def create_autoshop_task() -> None:
    create_count = core.celery_entry_point.get_create_count(AutoShop)

    car_count = Car.objects.filter(is_active=True).count()

    if create_count == 0:
        return

    autoshops_data = core.celery_entry_point.load_json_data('autoshops', 'autoshops.json')
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
            ) for car in Car.objects.filter(is_active=True).order_by('?')[:min(car_count, available_cars_amount)]]

            shop.cars_in_stock.set(available_cars)
            shop.save()

            created_count += 1

    print(f'Created {created_count} autoshops')

@shared_task
def create_offers_task() -> None:
    shops = AutoShop.objects.all().filter(is_active=True)
    for shop in shops:
        create_offer(shop)


@shared_task
def purchase_cars_by_shops_from_supplier_task() -> None:
    shop_offers = AutoShopOffer.objects.filter(is_active=True).all()
    suppliers = Supplier.objects.filter(is_active=True).all()
    sales = SupplierSale.objects.filter(is_active=True).all()

    purchase_cars_by_shops_from_suppliers(sales, shop_offers, suppliers)

def get_suitable_suppliers(shop: AutoShop, suppliers: List[Supplier]) -> Dict[Supplier, List[AvailableCars]]:
    suitable_suppliers = {}
    for supplier in suppliers:
        for car_in_stock in supplier.cars_in_stock.all():
            car = car_in_stock.car

            if (car.is_active and
               (shop.desired_model == car.model) and
               (shop.desired_brand == car.brand) and
               (shop.max_horsepower >= car.horsepower >= shop.min_horsepower) and
               (shop.max_year >= car.year >= shop.min_year)):
                    if not suitable_suppliers.keys().__contains__(supplier):
                        suitable_suppliers[supplier] = list()
                    suitable_suppliers[supplier].append(car_in_stock)

    return suitable_suppliers

def pick_car_to_buy(sales: List[SupplierSale], cars_by_suppliers: Dict[Supplier, List[AvailableCars]]) -> AvailableCars:
    car_to_popularity = {}
    checked_cars = set()
    for supplier, cars in cars_by_suppliers.items():
        for car in cars:
            if not car in checked_cars:
                car_to_popularity[car] = sum(1 for sale in sales if sale.car == car.car)
                checked_cars.add(car)

    if len(car_to_popularity) > 0 and random.choice(range(2)) == 1:
        return max(car_to_popularity, key=car_to_popularity.get)

    return random.choice(random.choice(list(cars_by_suppliers.items()))[1])

def get_best_supplier_by_price(desired_car: Car, shop: AutoShop, cars_by_suppliers: Dict[Supplier, List[AvailableCars]]) -> Tuple[Supplier, float, float]:
    filtered_suppliers = {}

    for supplier, available_cars in cars_by_suppliers.items():
        for available_car in available_cars:
            if available_car.car==desired_car:
                filtered_suppliers[supplier] = available_car.price


    discounts_for_autoshop = list(AutoShopPersonalDiscount.objects.filter(autoshop=shop).all())

    return core.celery_entry_point.get_best_by_price(filtered_suppliers, discounts_for_autoshop, desired_car, shop)


def buy(shop: AutoShop, car: AvailableCars, price: float) -> None:
    shop.purchase_car(car.car, price)
    car.last_purchase_date = datetime.now()


def add_sales_history(shop: AutoShop, supplier: Supplier, car: Car, price: float, discount_percent: float) -> None:
    sale = SupplierSale.objects.create(
        car=car,
        price=price,
        discount_percent=discount_percent,
        date=datetime.now(),
        supplier=supplier,
        autoshop=shop
    )
    sale.save()
    print(f"Successful purchase: {supplier} -> {car} -> {shop} for {price}")


def create_offer(shop: AutoShop) -> AutoShopOffer | None:

    if AutoShopOffer.objects.filter(is_active=True).filter(autoshop=shop).exists(): return

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

def purchase_cars_by_shops_from_suppliers(sales: List[SupplierSale], autoshop_offers: List[AutoShopOffer], suppliers: List[Supplier]) -> None:
    for offer in autoshop_offers:
        shop = offer.autoshop
        suitable_suppliers = get_suitable_suppliers(shop, suppliers)

        if len(suitable_suppliers) == 0:
            continue

        desired_car = pick_car_to_buy(sales, suitable_suppliers)
        best_supplier, price, discount = get_best_supplier_by_price(desired_car.car, shop, suitable_suppliers)

        if shop.balance >= price:
            buy(shop, desired_car, price)
            add_sales_history(shop, best_supplier, desired_car.car, price, discount)
            offer.is_active = False
            offer.save()
