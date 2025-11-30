import random
from typing import Dict, Tuple

from celery import shared_task
from django.db.models import Prefetch
from django.utils import timezone

import core
import core.celery_base
from autoshops.models import AutoShop
from available_cars.models import AvailableCars
from cars.models import Car
from core.celery_base import get_create_count, load_json_data
from core.configs.celery_config import CeleryConfig
from discounts.models import UserPersonalDiscount
from offers.models import UserOffer
from sales.models import AutoShopSale
from users.models import User


@shared_task
def create_user_task() -> None:
    create_count = get_create_count(User)
    if create_count == 0:
        return
    users_data = load_json_data('users', 'users.json')
    if not users_data:
        return
    created_count = 0
    random.shuffle(users_data)
    for user_data in users_data[:create_count]:
        if not User.objects.filter(email=user_data['email']).exists():
            User.objects.create(**user_data)
            created_count += 1
    return


@shared_task
def create_offer_for_users() -> None:
    users = User.objects.all().filter(is_active=True)
    for user in users:
        create_offer_for_user(user)


@shared_task
def add_random_balance_for_users() -> None:
    users = User.objects.all().filter(is_active=True)
    for user in users:
        user.balance += CeleryConfig.get_random_user_income()
        user.save()


@shared_task
def purchase_car_by_offers_task() -> None:
    shop_offers = UserOffer.objects.filter(is_active=True).all()

    for offer in shop_offers:
        user = offer.user
        suitable_shops = get_suitable_shops(offer)

        if len(suitable_shops) == 0:
            continue

        desired_car = offer.car
        shop, price, discount, available_car = get_best_shop_by_price(desired_car, user, suitable_shops)

        if user.balance >= price:
            buy(user, price)
            shop.try_add_buyer(user)
            shop.reduce_car_amount(available_car)
            add_sales_history(shop, user, desired_car, price, discount)
            offer.is_active = False
            offer.save()


def get_suitable_shops(user_offer: UserOffer) -> Dict[AutoShop, AvailableCars]:

    query = AutoShop.objects.filter(
        is_active=True,
        cars_in_stock__car=user_offer.car,
        cars_in_stock__car__is_active=True,
    ).prefetch_related(Prefetch(
        'cars_in_stock',
        queryset=AvailableCars.objects.filter(
            car=user_offer.car,
            is_active=True,
        )
    ))

    return {shop: shop.cars_in_stock.first() for shop in query}


def get_best_shop_by_price(car: Car, user: User, cars_by_shops: Dict[AutoShop, AvailableCars]) -> Tuple[AutoShop, float, float, AvailableCars]:
    filtered_shops = {}
    car_by_shop = {}

    for shop, available_car in cars_by_shops.items():
        if available_car.car == car:
            filtered_shops[shop] = available_car.price
            car_by_shop[shop] = available_car

    discounts_for_user = list(UserPersonalDiscount.objects.filter(user=user))
    shop, price, discount = core.celery_base.get_best_by_price(filtered_shops, discounts_for_user, car, user)

    return shop, price, discount, car_by_shop[shop]


def buy(user: User, price: float) -> None:
    user.purchase_car(price)


def add_sales_history(shop: AutoShop, user: User, car: Car, price: float, discount_percent: float) -> None:
    sale = AutoShopSale.objects.create(
        user=user,
        car=car,
        price=price,
        discount_percent=discount_percent,
        date=timezone.now(),
        autoshop=shop
    )
    sale.save()
    print(f"Successful purchase: {user} -> {car} -> {shop} for {price}")


def create_offer_for_user(user: User) -> UserOffer | None:
    if UserOffer.objects.filter(is_active=True).filter(user=user).exists():
        return None

    if random.randint(0, 1):
        autoshops_with_cars = (AutoShop.objects
                               .filter(is_active=True, cars_in_stock__isnull=False, cars_in_stock__amount__gt=0)
                               .all())

        if not autoshops_with_cars:
            return None

        car = (random.choice(
            random.choice(autoshops_with_cars).cars_in_stock.filter(is_active=True).all())).car

    else:
        car = random.choice(Car.objects.filter(is_active=True).all())

    if UserOffer.objects.filter(is_active=True).filter(car=car).exists():
        return None

    if not car:
        return None

    price = core.celery_base.get_min_max_car_price(user.balance)

    if not price:
        return None

    _, max_price = price

    offer = UserOffer.objects.create(
        user=user,
        car=car,
        max_price=min(max_price, user.balance)
    )

    offer.save()
    return offer
