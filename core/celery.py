import os
from datetime import datetime
from typing import Tuple, Any, Dict, List
from celery import Celery

from cars.models import Car
from core.configs.simulation_config import SimulationConfig

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

def get_min_max_price(balance: float) -> Tuple[float, float] | None:
    min_price, max_price = SimulationConfig.MIN_MAX_CAR_RANDOM_PRICE
    if min_price < balance: return None
    max_price = max_price if balance >= max_price else balance
    return min_price, max_price

def get_best_by_price(filtered: Dict[Any, Any], discounts: List[Any], car: Car) -> Tuple[Any, float, float]:
    prices_per_car: Dict[Any, float] = {}
    total_discount_percent: float = 0

    for item, price in filtered:
        filtered = list(
            filter(lambda x: x.shop == item, discounts))
        total_discount_percent = 0
        if len(filtered) > 0:
            discount = filtered[0]
            total_discount_percent += discount.get_full_discount_percent()

        car_discount = list(filter(lambda x: x.car == car, item.car_discounts))
        if len(car_discount) > 0:
            total_discount_percent += car_discount[0].percent

        current_date = datetime.now()

        if item.general_discount_id.start_date >= current_date >= item.general_discount_id.end_date:
            total_discount_percent += item.general_discount_id.percent

        result_price = price - (total_discount_percent / 100 * price)
        result_price = result_price if result_price > 0 else 0
        prices_per_car[item] = result_price

    result = (sorted(prices_per_car.items(), key=lambda x: x[1], reverse=True))[0]

    return result[0], result[1], total_discount_percent