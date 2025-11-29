import random
from typing import Tuple
from decouple import config

class CeleryConfig:
    MAX_ACTIVE_ENTITIES_PER_MODEL = config("MAX_ACTIVE_ENTITIES_PER_MODEL", cast=int, default=50)
    DEFAULT_SCHEDULE_SECONDS = config("DEFAULT_SCHEDULE_SECONDS", cast=float, default=30)
    CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")
    CELERY_BROKER_URL = config("CELERY_BROKER_URL")
    CELERY_CACHE_BACKEND = config("CELERY_CACHE_BACKEND")
    SUPPLIER_MAX_AVAILABLE_CARS_AMOUNT = config("SUPPLIER_MAX_AVAILABLE_CARS_AMOUNT", cast=int)

    _cashed_autoshop_balance = None
    _cashed_user_balance = None
    _cashed_user_income = None
    _cashed_car_price = None

    @staticmethod
    def get_min_max_car_price() -> tuple:
        CeleryConfig._cashed_car_price, _ = CeleryConfig._get_random_value_from_tuple(CeleryConfig._cashed_car_price, "MIN_MAX_CAR_RANDOM_PRICE")
        return CeleryConfig._cashed_car_price

    @staticmethod
    def get_random_autoshop_start_balance() -> float:
        CeleryConfig._cashed_autoshop_balance, balance = CeleryConfig._get_random_value_from_tuple(CeleryConfig._cashed_autoshop_balance, "MIN_MAX_CAR_RANDOM_AUTOSHOP_START_BALANCE")
        return balance

    @staticmethod
    def get_random_user_start_balance() -> float:
        CeleryConfig._cashed_user_balance, balance = CeleryConfig._get_random_value_from_tuple(CeleryConfig._cashed_user_balance, "MIN_MAX_CAR_RANDOM_USER_START_BALANCE")
        return balance

    @staticmethod
    def get_random_user_income() -> float:
        CeleryConfig._cashed_user_income, income = CeleryConfig._get_random_value_from_tuple(CeleryConfig._cashed_user_income, "MIN_MAX_RANDOM_USER_INCOME")
        return income

    @staticmethod
    def get_random_car_price() -> float:
        CeleryConfig._cashed_car_price, price = CeleryConfig._get_random_value_from_tuple(CeleryConfig._cashed_car_price, "MIN_MAX_CAR_RANDOM_PRICE")
        return price

    @staticmethod
    def _get_float_tuple(value) -> tuple:
        return tuple(float(x) for x in (config(value).split(',')))

    @staticmethod
    def _get_random_value_from_tuple(data, name) -> Tuple[Tuple, float]:
        if not data:
            data = CeleryConfig._get_float_tuple(name)

        return data, round(random.uniform(*data), 2)

    CELERY_BEAT_SCHEDULE = {
    'create_autoshop_task':
        {
            'task': 'autoshops.tasks.create_autoshop_task',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'delete_autoshop_task':
        {
            'task': 'autoshops.tasks.delete_autoshop_task',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'autoshops.tasks.create_offers_task':
        {
            'task': 'autoshops.tasks.create_offers_task',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'purchase_cars_by_shops_from_supplier_task':
        {
            'task': 'autoshops.tasks.purchase_cars_by_shops_from_supplier_task',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'create_cars_from_json':
        {
            'task': 'cars.tasks.create_cars_from_json',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'remove_ended_discounts_task':
        {
            'task': 'discounts.tasks.remove_ended_discounts_task',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'create_general_discounts_from_json':
        {
            'task': 'discounts.tasks.create_general_discounts_from_json',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'create_car_discounts_from_json':
        {
            'task': 'discounts.tasks.create_car_discounts_from_json',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'create_user_personal_discounts_from_json':
        {
            'task': 'discounts.tasks.create_user_personal_discounts_from_json',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'create_suppliers_from_json':
        {
            'task': 'suppliers.tasks.create_suppliers_from_json',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'create_user_task':
        {
            'task': 'users.tasks.create_user_task',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'create_offer_for_users':
        {
            'task': 'users.tasks.create_offer_for_users',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'add_random_balance_for_users':
        {
            'task': 'users.tasks.add_random_balance_for_users',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'purchase_car_by_offers_task':
        {
            'task': 'users.tasks.purchase_car_by_offers_task',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'add_available_cars':
        {
            'task': 'suppliers.tasks.add_available_cars',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'add_discount_on_supplier_cars':
        {
            'task': 'suppliers.tasks.add_discount_on_cars',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
    'add_discount_on_autoshop_cars':
        {
            'task': 'autoshops.tasks.add_discount_on_cars',
            'schedule': DEFAULT_SCHEDULE_SECONDS
        },
}