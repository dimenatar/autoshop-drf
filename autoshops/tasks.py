import random
from datetime import datetime
from typing import Dict, Tuple, List
from celery import shared_task

import core.celery
from autoshops.models import AutoShop
from available_cars.models import AvailableCars
from cars.models import Car
from discounts.models import AutoShopPersonalDiscount
from offers.models import AutoShopOffer
from sales.models import SupplierSale
from suppliers.models import Supplier


@shared_task
def delete_autoshop_task() -> None:
    shops = AutoShop.objects.all().filter(is_active=True)
    company_worth_by_autoshop = {}

    for shop in shops:
        company_worth_by_autoshop[shop] = sum([car.amount * car.price for car in shop.cars_in_stock]) + shop.balance

    sorted_shops = list(sorted(company_worth_by_autoshop, key=lambda x:x[1], reverse=False))
    if not sorted_shops: return

    bankrupt = sorted_shops[0][0]
    bankrupt.is_active = False
    bankrupt.save()

    found_offers = AutoShopOffer.objects.all().filter(autoshop=bankrupt)
    for offer in found_offers:
        offer.is_active = False
        offer.save()


@shared_task
def create_autoshop_task() -> None:

    pass

@shared_task
def create_offers_task() -> None:
    shops = AutoShop.objects.all().filter(is_active=True)
    for shop in shops:
        create_offer(shop)


@shared_task
def purchase_cars_by_shops_from_supplier_task() -> None:
    shop_offers = AutoShopOffer.objects.all()
    suppliers = Supplier.objects.all().filter(is_active=True)
    sales = SupplierSale.objects.all().filter(is_active=True)


    purchase_cars_by_shops_from_suppliers(sales, shop_offers, suppliers)

def get_suitable_suppliers(shop: AutoShop, suppliers: List[Supplier]) -> Dict[Supplier, List[AvailableCars]]:
    suitable_suppliers = {}
    for supplier in suppliers:
        for car_in_stock in supplier.cars_in_stock.all():
            car = car_in_stock.car_id
            if (car.is_active and
               (shop.desired_model == car.desired_model) and
               (shop.desired_brand == car.desired_brand) and
               (shop.max_horsepower >= car.horsepower >= shop.min_horsepower) and
               (shop.max_year >= car.year >= shop.min_year)):
                    if not suitable_suppliers.keys().__contains__(supplier):
                        suitable_suppliers[supplier] = list()
                    suitable_suppliers[supplier].append(car_in_stock)

    return suitable_suppliers

def pick_car_to_buy(sales: List[SupplierSale], cars_by_suppliers: Dict[Supplier, List[AvailableCars]]) -> Car:
    car_to_popularity = {}
    checked_cars = set()
    for supplier, cars in cars_by_suppliers:
        for car in cars:
            if not car in checked_cars:
                car_to_popularity[car] = sales.count(car)
                checked_cars.add(car)

    if len(car_to_popularity) > 0 and random.choice(range(2)) == 1:
        return (sorted(car_to_popularity.items(), key=lambda x: x[1], reverse=True))[0][0]

    return random.choice(random.choice(list(cars_by_suppliers))[1])

def get_best_supplier_by_price(desired_car: Car, shop: AutoShop, cars_by_suppliers: Dict[Supplier, List[AvailableCars]]) -> Tuple[Supplier, float, float]:
    filtered_suppliers = {}

    for supplier, available_cars in cars_by_suppliers:
        for available_car in available_cars:
            if available_car.car_id==desired_car:
                filtered_suppliers[supplier] = available_car.price


    discounts_for_autoshop = list(AutoShopPersonalDiscount.objects.filter(autoshop=shop).all())

    return core.celery.get_best_by_price(filtered_suppliers, discounts_for_autoshop, desired_car)

    #prices_per_car: Dict[Supplier, float] = {}
    #total_discount_percent: float = 0
#
    #for supplier, price in filtered_suppliers:
    #    filtered: List[AutoShopPersonalDiscount] = list(filter(lambda x: x.supplier==supplier, discounts_for_autoshop))
    #    total_discount_percent = 0
    #    if len(filtered) > 0:
    #        discount = filtered[0]
    #        total_discount_percent += discount.get_full_discount_percent()
#
    #    car_discount = list(filter(lambda x: x.car==desired_car, supplier.car_discounts))
    #    if len(car_discount) > 0:
    #        total_discount_percent += car_discount[0].percent
#
    #    current_date = datetime.now()
#
    #    if supplier.general_discount_id.start_date >= current_date >= supplier.general_discount_id.end_date:
    #        total_discount_percent += supplier.general_discount_id.percent
#
    #    result_price = price - (total_discount_percent / 100 * price)
    #    result_price = result_price if result_price > 0 else 0
    #    prices_per_car[supplier] = result_price
#
    #best_supplier = (sorted(prices_per_car.items(), key=lambda x: x[1], reverse=True))[0]
#
    #return best_supplier[0], best_supplier[1], total_discount_percent


def buy(shop: AutoShop, car: Car, price: float) -> None:
    shop.purchase_car(car, price)


def add_sales_history(shop: AutoShop, supplier: Supplier, car: Car, price: float, discount_percent: float) -> None:
    sale = SupplierSale.objects.create(
        car_id=car,
        price=price,
        discount_percent=discount_percent,
        date=datetime.now(),
        supplier_id=supplier,
        autoshop_id=shop
    )
    sale.save()
    print(f"Successful purchase: {supplier} -> {car} -> {shop} for {price}")


def create_offer(shop) -> AutoShopOffer | None:
    car = Car.objects.all().filter(
        model=shop.desired_model,
        brand=shop.desired_brand,
        year__range=[shop.min_year, shop.max_year],
        horsepower__range=[shop.min_horsepower, shop.max_horsepower],
    ).first()

    if not car: return None

    price = core.celery.get_min_max_price(shop.balance)

    if not price: return None

    min_price, max_price = price

    offer = AutoShopOffer.objects.create(
        autoshop=shop,
        car=car,
        desired_brand=shop.desired_brand,
        desired_model=shop.desired_model,
        min_horsepower=shop.min_horsepower,
        max_horsepower=shop.max_horsepower,
        min_year=shop.min_year,
        max_year=shop.max_year,
        max_price=max_price,
        min_price=min_price,
    )

    offer.save()
    return offer

def purchase_cars_by_shops_from_suppliers(sales: List[SupplierSale], autoshop_offers: List[AutoShopOffer], suppliers: List[Supplier]) -> None:
    for offer in autoshop_offers:
        shop = offer.autoshop
        suitable_suppliers = get_suitable_suppliers(shop, suppliers)

        if len(suitable_suppliers) == 0:
            print(f"No suitable suppliers for shop {shop.name}")
            continue

        desired_car = pick_car_to_buy(sales, suitable_suppliers)
        best_supplier, price, discount = get_best_supplier_by_price(desired_car, shop, suitable_suppliers)

        if shop.balance >= price:
            buy(shop, desired_car, price)
            add_sales_history(shop, best_supplier, desired_car, price, discount)
        else:
            print(f"Shop {shop.name} does not has enough balance for minimum price {price}")
