import json
import os
import pathlib
from datetime import datetime
from django.utils import timezone
import random
from typing import Tuple, Any, Dict, List
from celery import Celery

from core.configs.celery_config import CeleryConfig

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

def get_min_max_car_price(balance: float) -> Tuple[float, float] | None:
    min_price, max_price = CeleryConfig.get_min_max_car_price()
    if min_price > balance:
        return None
    max_price = min(max_price, balance)
    return min_price, max_price

def get_best_by_price(price_by_entity: Dict[Any, Any], discounts: List[Any], car: Any, buyer: Any) -> Tuple[Any, float, float]:
    prices_per_car: Dict[Any, Any] = {}
    total_discount_percent: float = 0

    for item, price in price_by_entity.items():
        personal_discounts = [pd for pd in discounts if pd.is_suitable_discount(item, buyer)]
        total_discount_percent = 0
        if personal_discounts:
            discount = personal_discounts[0]
            total_discount_percent += discount.get_full_discount_percent()

        car_discounts = [cd for cd in item.car_discounts.filter(is_active=True).all() if cd.cars.contains(car)]
        if car_discounts:
            total_discount_percent += car_discounts[0].percent

        current_date = datetime.now().date()

        if item.general_discount and item.general_discount.start_date <= current_date <= item.general_discount.end_date:
            total_discount_percent += item.general_discount.percent

        result_price = price - (total_discount_percent / 100 * price)
        result_price = result_price if result_price > 0 else 0

        prices_per_car[item] = (result_price, total_discount_percent)

    best_item, (best_price, best_discount) = min(prices_per_car.items(), key=lambda x: x[1][0])

    return best_item, best_price, best_discount

def get_available_count(model) -> int:
    return model.objects.filter(is_active=True).count()

def get_create_count(model) -> int:
    current_count = get_available_count(model)
    available_slots = CeleryConfig.MAX_ACTIVE_ENTITIES_PER_MODEL - current_count
    return min(10, random.randrange(min(CeleryConfig.MAX_ACTIVE_ENTITIES_PER_MODEL, available_slots))) if available_slots > 0 else 0

def generate_discounts(entities: List[Any]) -> None:
    now = timezone.now()
    from discounts.models import CarDiscount

    for entity in entities:
        poorly_sellings = entity.cars_in_stock.filter(
            is_active=True,
            last_purchase_date__lte=now - timezone.timedelta(seconds=120)
        ).select_related('car')

        if not poorly_sellings.exists():
            continue

        car_ids = list(poorly_sellings.values_list('car_id', flat=True))

        existing_discounts_map = {}
        existing_discounts = entity.car_discounts.filter(
            is_active=True,
            cars__id__in=car_ids
        ).prefetch_related('cars')

        for discount in existing_discounts:
            for car in discount.cars.all():
                existing_discounts_map[car.id] = discount

        discounts_to_update = []
        new_discounts_data = []
        cars_for_new_discounts = []

        for poorly_selling in poorly_sellings:

            car_id = poorly_selling.car_id

            if car_id in existing_discounts_map:
                discount = existing_discounts_map[car_id]
                discount.percent += 5
                discounts_to_update.append(discount)
            else:
                new_discounts_data.append(CarDiscount(percent=5))
                cars_for_new_discounts.append(car_id)

        if discounts_to_update:
            CarDiscount.objects.bulk_update(discounts_to_update, ['percent'])

        if new_discounts_data:
            new_discounts = CarDiscount.objects.bulk_create(new_discounts_data)

            through_relations = []
            for discount, car_id in zip(new_discounts, cars_for_new_discounts):
                through_relations.append(
                    CarDiscount.cars.through(
                        cardiscount_id=discount.id,
                        car_id=car_id
                    )
                )

            CarDiscount.cars.through.objects.bulk_create(through_relations)
            entity.car_discounts.add(*new_discounts)

def load_json_data(package, filename) -> List[Any]:
    path_to_project = pathlib.Path(__file__).parent.parent.absolute()

    try:
        with open(os.path.join(path_to_project, package, filename), 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []