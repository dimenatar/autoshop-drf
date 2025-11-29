import random

from celery import shared_task

from cars.models import Car
from core.celery_entry_point import get_create_count, load_json_data


@shared_task
def create_cars_from_json() -> dict | None:
    create_count = get_create_count(Car)
    if create_count == 0:
        return {
            'status': "error. create count is 0",
        }

    cars_data = load_json_data('cars', 'cars.json')
    if not cars_data:
        return {
            'status': "error. didn't find any cars.",
        }

    created_count = 0

    random.shuffle(cars_data)

    for car_data in cars_data[:create_count]:
        if not Car.objects.filter(
                model=car_data['model'],
                brand=car_data['brand'],
                year=car_data['year'],
                horsepower=car_data['horsepower']
        ).exists():
            Car.objects.create(**car_data)
            created_count += 1

    return {
        'created': created_count,
    }
