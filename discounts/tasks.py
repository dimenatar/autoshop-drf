import random
from datetime import datetime

from celery import shared_task
from faker.proxy import Faker

from autoshops.models import AutoShop
from cars.models import Car
from core.celery_entry_point import get_create_count, load_json_data
from discounts.models import GeneralDiscount, CarDiscount, UserPersonalDiscount
from users.models import User

DISCOUNT_THEMES = [
    "seasonal", "holiday", "clearance", "loyalty", "promotional",
    "anniversary", "special", "limited", "exclusive", "premium"
]

DISCOUNT_TYPES = [
    "Sale", "Discount", "Offer", "Promotion", "Deal",
    "Bonus", "Reward", "Special", "Event", "Clearance"
]

ADJECTIVES = [
    "Amazing", "Incredible", "Fantastic", "Super", "Mega",
    "Ultimate", "Premium", "Exclusive", "Limited", "Special",
    "Grand", "Big", "Huge", "Massive", "Epic"
]

@shared_task
def remove_ended_discounts_task() -> None:
    discounts = GeneralDiscount.objects.filter(is_active=True).all()
    current_date = datetime.now().date()

    for discount in discounts:
        if current_date > discount.end_date:
            discount.is_active = False
            discount.save()


@shared_task
def create_general_discounts_from_json():
    create_count = get_create_count(GeneralDiscount)
    if create_count == 0:
        return

    discounts_data = load_json_data('discounts', 'general_discounts.json')
    if not discounts_data:
        return

    created_count = 0
    random.shuffle(discounts_data)

    for discount_data in discounts_data[:create_count]:
        if not GeneralDiscount.objects.filter(name=discount_data['name']).exists():
            from datetime import datetime
            discount_data['start_date'] = datetime.strptime(discount_data['start_date'], '%Y-%m-%d').date()
            discount_data['end_date'] = datetime.strptime(discount_data['end_date'], '%Y-%m-%d').date()

            GeneralDiscount.objects.create(**discount_data)
            created_count += 1


@shared_task
def create_car_discounts_from_json() -> None:
    create_count = get_create_count(CarDiscount)
    if create_count == 0:
        return

    car_discounts_data = load_json_data('discounts', 'car_discounts.json')
    if not car_discounts_data:
        return

    existing_cars = {car.id: car for car in Car.objects.filter(is_active=True)}
    if not existing_cars:
        return

    created_count = 0
    random.shuffle(car_discounts_data)

    for discount_data in car_discounts_data[:create_count]:
        car_discount, created = CarDiscount.objects.get_or_create(
            percent=discount_data['percent']
        )

        if created:
            car_ids = discount_data.get('cars', [])
            cars_to_add = [existing_cars[car_id] for car_id in car_ids if car_id in existing_cars]
            if cars_to_add:
                car_discount.cars.set(cars_to_add)
                created_count += 1
            else:
                car_discount.is_active = False
                car_discount.save()


@shared_task
def create_user_personal_discounts_from_json() -> None:
    create_count = get_create_count(UserPersonalDiscount)
    if create_count == 0:
        return

    discounts_data = load_json_data('discounts', 'user_personal_discounts.json')
    if not discounts_data:
        return

    existing_users = {user.id: user for user in User.objects.filter(is_active=True, role='customer')}
    existing_autoshops = {autoshop.id: autoshop for autoshop in AutoShop.objects.filter(is_active=True)}

    if not existing_users or not existing_autoshops:
        return

    created_count = 0
    random.shuffle(discounts_data)

    for discount_data in discounts_data[:create_count]:
        user_id = discount_data['user_id']
        autoshop_id = discount_data['autoshop_id']

        if user_id not in existing_users or autoshop_id not in existing_autoshops:
            continue

        if not UserPersonalDiscount.objects.filter(
                user=existing_users[user_id],
                autoshop=existing_autoshops[autoshop_id]
        ).exists():
            UserPersonalDiscount.objects.create(
                percent=discount_data['percent'],
                purchases_amount=discount_data['purchases_amount'],
                user=existing_users[user_id],
                autoshop=existing_autoshops[autoshop_id]
            )
            created_count += 1

def get_random_discount_name() -> str:
    return f'{random.choice(ADJECTIVES)} {random.choice(DISCOUNT_THEMES)} {random.choice(DISCOUNT_TYPES)}'

def get_random_discount_description() -> str:
    return Faker().text(max_nb_chars=100)