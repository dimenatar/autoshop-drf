from datetime import datetime
import random
from typing import Dict, List, Tuple

from celery import shared_task

import core
from autoshops.models import AutoShop
from available_cars.models import AvailableCars
from cars.models import Car
from core.configs.simulation_config import SimulationConfig
from discounts.models import AutoShopPersonalDiscount, UserPersonalDiscount
from offers.models import UserOffer, AutoShopOffer
from sales.models import AutoShopSale
from users.models import User


@shared_task
def create_user_task() -> None:
    pass

@shared_task
def create_offer_for_users() -> None:
    users = User.objects.all().filter(is_active=True)
    for user in users:
        create_offer_for_user(user)

@shared_task
def add_random_balance_for_users() -> None:
    min_balance, max_balance = SimulationConfig.MIN_MAX_CAR_RANDOM_USER_INCOME
    users = User.objects.all().filter(is_active=True)
    for user in users:
        user.balance += random.randint(min_balance, max_balance)
        user.save()

@shared_task
def purchase_car_by_offers_task() -> None:
    shop_offers = AutoShopOffer.objects.all().filter(is_active=True)
    autoshops = AutoShop.objects.all().filter(is_active=True)

    purchase_cars_by_users_from_shops(shop_offers, autoshops)

def get_suitable_shops(user_offer: UserOffer, shops: List[AutoShop]) -> Dict[AutoShop, AvailableCars]:
    suitable_shops = {}
    for shop in shops:
        for car_in_stock in shop.cars_in_stock.all():
            car = car_in_stock.car_id
            if car.is_active and car == user_offer.car:
                suitable_shops[shop] = car_in_stock

    return suitable_shops

def get_best_shop_by_price(car: Car, user: User, cars_by_shops: Dict[AutoShop, AvailableCars]) -> Tuple[AutoShop, float, float]:
    filtered_shops = {}

    for shop, available_car in cars_by_shops:
        if available_car.car_id == car:
            filtered_shops[shop] = available_car.price


    discounts_for_user = list(UserPersonalDiscount.objects.filter(user=user))

    return core.celery.get_best_by_price(filtered_shops, discounts_for_user, car)

    #prices_per_car: Dict[AutoShop, float] = {}
    #total_discount_percent: float = 0
#
    #for shop, price in filtered_shops:
    #    filtered: List[AutoShopPersonalDiscount] = list(
    #        filter(lambda x: x.shop == shop, discounts_for_user))
    #    total_discount_percent = 0
    #    if len(filtered) > 0:
    #        discount = filtered[0]
    #        total_discount_percent += discount.get_full_discount_percent()
#
    #    car_discount = list(filter(lambda x: x.car == car, shop.car_discounts))
    #    if len(car_discount) > 0:
    #        total_discount_percent += car_discount[0].percent
#
    #    current_date = datetime.now()
#
    #    if shop.general_discount_id.start_date >= current_date >= shop.general_discount_id.end_date:
    #        total_discount_percent += shop.general_discount_id.percent
#
    #    result_price = price - (total_discount_percent / 100 * price)
    #    result_price = result_price if result_price > 0 else 0
    #    prices_per_car[shop] = result_price

    #best_shop = (sorted(prices_per_car.items(), key=lambda x: x[1], reverse=True))[0]

    #return best_shop[0], best_shop[1], total_discount_percent

def buy(user: User, car: Car, price: float) -> None:
    user.purchase_car(car, price)

def add_sales_history(shop: AutoShop, user: User, car: Car, price: float, discount_percent: float) -> None:
    sale = AutoShopSale.objects.create(
        user_id=user,
        car_id=car,
        price=price,
        discount_percent=discount_percent,
        date=datetime.now(),
        autoshop_id=shop
    )
    sale.save()
    print(f"Successful purchase: {user} -> {car} -> {shop} for {price}")

def purchase_cars_by_users_from_shops(offers: List[UserOffer], shops: List[AutoShop]) -> None:
    for offer in offers:
        user = offer.user
        suitable_shops = get_suitable_shops(offer, shops)

        if len(suitable_shops) == 0:
            print(f"No suitable suppliers for shop {user.name}")
            continue

        desired_car = offer.car
        shop, price, discount = get_best_shop_by_price(desired_car, user, suitable_shops)

        if user.balance >= price:
            buy(user, desired_car, price)
            add_sales_history(shop, user, desired_car, price, discount)
        else:
            print(f"Shop {user.name} does not has enough balance for minimum price {price}")


def create_offer_for_user(user: User) -> UserOffer | None:
    car = random.choice(Car.objects.all())
    if not car: return None
    price = core.celery.get_min_max_price(user.balance)
    if not price: return None

    _, max_price = price

    offer = UserOffer.objects.create(
        user=user,
        car=car,
        max_price=max_price,
    )

    offer.save()
    return offer
