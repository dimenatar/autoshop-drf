import random
from datetime import datetime, timedelta
from typing import Tuple, List, Any

from celery import shared_task

from core.configs.simulation_config import SimulationConfig
from discounts.models import GeneralDiscount


@shared_task
def remove_ended_discounts_task() -> None:
    discounts = GeneralDiscount.objects.filter(is_active=True).all()
    current_date = datetime.now()

    for discount in discounts:
        if current_date > discount.end_date:
            discount.is_active = False
            discount.save()


def get_random_discount_name():
    pass


def get_random_discount_description():
    pass


@shared_task
def create_discounts_task() -> None:
    general_discounts = GeneralDiscount.objects.filter(is_active=True).all()
    is_need, amount = is_need_to_create_discounts(general_discounts)
    if is_need:
        for i in range(amount):
            create_general_discount()




def create_general_discount() -> None:
    hours_offset = random.randint(0, 4)
    hour_duration = random.randint(0, 4)
    now = datetime.now()
    discount = GeneralDiscount.objects.create(
        start_date=now + timedelta(hours=hours_offset),
        end_date=now + timedelta(hours=hours_offset + hour_duration),
        name=get_random_discount_name(),
        desciption=get_random_discount_description(),
    )


def is_need_to_create_discounts(discounts: List[Any]) -> Tuple[bool, int]:
    length = len(discounts)
    return length < SimulationConfig.MAX_ACTIVE_ENTITIES_PER_MODEL, SimulationConfig.MAX_ACTIVE_ENTITIES_PER_MODEL - length
