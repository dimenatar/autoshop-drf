import random

from celery import shared_task

import core
from available_cars.models import AvailableCars
from cars.models import Car
from core.celery_entry_point import get_create_count, load_json_data
from core.configs.celery_config import CeleryConfig
from discounts.models import GeneralDiscount
from suppliers.models import Supplier


@shared_task
def add_discount_on_cars() -> None:
    suppliers = Supplier.objects.filter(is_active=True).all()
    core.celery_entry_point.generate_discounts(suppliers)


@shared_task
def add_available_cars() -> None:
    if Car.objects.filter(is_active=True).count() == 0:
        return

    for supplier in Supplier.objects.filter(is_active=True).all():
        car_amount_to_add = CeleryConfig.SUPPLIER_MAX_AVAILABLE_CARS_AMOUNT - supplier.cars_in_stock.filter(is_active=True).count()
        if car_amount_to_add > 0:
            supplier_existing_car_id = [car.car.id for car in supplier.cars_in_stock.all()]
            car_amount_to_add = min(10, car_amount_to_add)
            for _ in range(car_amount_to_add):

                cars_to_choose = Car.objects.filter(
                    is_active=True
                ).exclude(
                    id__in=supplier_existing_car_id
                )

                if not cars_to_choose:
                    break

                car = random.choice(cars_to_choose)

                created_car = AvailableCars.objects.create(
                    car=car,
                    price=CeleryConfig.get_random_car_price(),
                    amount=random.randint(1, 10)
                )
                created_car.save()
                supplier_existing_car_id.append(car.id)
                supplier.cars_in_stock.add(created_car)


@shared_task
def create_suppliers_from_json() -> None:
    create_count = get_create_count(Supplier)
    if create_count == 0:
        return

    suppliers_data = load_json_data('suppliers', 'suppliers.json')
    if not suppliers_data:
        return

    existing_discounts = {discount.id: discount for discount in GeneralDiscount.objects.filter(is_active=True)}

    created_count = 0
    random.shuffle(suppliers_data)

    for supplier_data in suppliers_data[:create_count]:
        if not Supplier.objects.filter(name=supplier_data['name']).exists():
            general_discount = None
            if supplier_data.get('general_discount_id') and supplier_data['general_discount_id'] in existing_discounts:
                general_discount = existing_discounts[supplier_data['general_discount_id']]

            Supplier.objects.create(
                name=supplier_data['name'],
                general_discount=general_discount
            )
            created_count += 1
