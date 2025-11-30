import json
import os.path
import pathlib
import random
from datetime import timedelta
from typing import Any, List

from faker import Faker

from core.configs.celery_config import CeleryConfig

fake = Faker()

COUNT = 5000

CAR_MODELS = {
    'Toyota': ['Camry', 'Corolla', 'Rav4', 'Highlander'],
    'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot'],
    'Ford': ['Fusion', 'Focus', 'Escape', 'Explorer'],
    'BMW': ['3 Series', '5 Series', 'X3', 'X5'],
    'Mercedes': ['C-Class', 'E-Class', 'GLC', 'GLE'],
    'Audi': ['A4', 'A6', 'Q5', 'Q7'],
    'Volkswagen': ['Golf', 'Passat', 'Tiguan', 'Atlas'],
    'Hyundai': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe'],
    'Kia': ['Optima', 'Sorento', 'Sportage', 'Telluride'],
    'Nissan': ['Altima', 'Maxima', 'Rogue', 'Murano']
}
COUNTRIES = ['US', 'CA', 'GB', 'DE', 'FR', 'JP', 'KR', 'CN', 'RU', 'BR']


def generate_cars(count: int) -> List[Any]:
    cars = []
    for i in range(count):
        brand = random.choice(list(CAR_MODELS.keys()))
        cars.append({
            'model': random.choice(CAR_MODELS[brand]),
            'brand': brand,
            'horsepower': random.randint(100, 500),
            'year': random.randint(2000, 2023)
        })
    return cars


def generate_users(count: int) -> List[Any]:
    users = []
    for i in range(count):
        users.append({
            'name': fake.name(),
            'age': random.randint(18, 80),
            'telephone': fake.phone_number()[:13],
            'balance': CeleryConfig.get_random_user_start_balance(),
            'role': 'customer',
            'password': fake.password(length=10),
            'email': fake.email()
        })
    return users


def generate_general_discounts(count: int) -> List[Any]:
    discounts = []
    for i in range(count):
        start_date = fake.date_between(start_date='-30d', end_date='today')
        end_date = start_date + timedelta(days=random.randint(1, 3))
        discounts.append({
            'percent': round(random.uniform(1, 20), 2),
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'name': fake.sentence(nb_words=3),
            'description': fake.text(max_nb_chars=200)
        })
    return discounts


def generate_suppliers(count: int, max_discount_id: int) -> List[Any]:
    suppliers = []
    for i in range(count):
        suppliers.append({
            'name': fake.company(),
            'general_discount_id': random.randint(1, max_discount_id) if random.random() > 0.3 else None
        })
    return suppliers


def generate_autoshops(count: int, max_discount_id: int) -> List[Any]:
    autoshops = []

    for i in range(count):
        balance = CeleryConfig.get_random_autoshop_start_balance()
        car_price = CeleryConfig.get_random_car_price()
        brand = random.choice(list(CAR_MODELS.keys()))
        autoshops.append({
            'name': fake.company(),
            'location': random.choice(COUNTRIES),
            'balance': balance,
            'max_price': car_price,
            'desired_brand': brand,
            'desired_model': random.choice(CAR_MODELS[brand]),
            'min_horsepower': random.randint(100, 300),
            'max_horsepower': random.randint(301, 500),
            'min_year': random.randint(2000, 2010),
            'max_year': random.randint(2011, 2023),
            'general_discount_id': random.randint(1, max_discount_id)
        })
    return autoshops


def generate_car_discounts(count: int, max_car_id: int) -> List[Any]:
    discounts = []
    for i in range(count):
        car_count = random.randint(1, 5)
        car_ids = random.sample(range(1, max_car_id+1), car_count)
        discounts.append({
            'percent': round(random.uniform(1, 15), 2),
            'cars': car_ids
        })
    return discounts


def generate_user_personal_discounts(count: int, max_user_id: int, max_autoshop_id: int) -> List[Any]:
    user_discounts = []
    for i in range(count):
        user_discounts.append({
            'percent': round(random.uniform(1, 10), 2),
            'purchases_amount': random.randint(1, 20),
            'user_id': random.randint(1, max_user_id),
            'autoshop_id': random.randint(1, max_autoshop_id)
        })
    return user_discounts


def write_to_file(package: str, filename: str, data: Any) -> None:
    path_to_project = pathlib.Path(__file__).parent.parent.absolute()

    with open(os.path.join(path_to_project, package, filename), 'w') as f:
        json.dump(data, f, indent=2)


def generate_autoshop_personal_discounts(count: int, max_autoshop_id: int, max_supplier_id: int) -> List[Any]:
    autoshop_discounts = []
    for i in range(count):
        autoshop_discounts.append({
            'percent': round(random.uniform(1, 10), 2),
            'purchases_amount': random.randint(1, 20),
            'autoshop_id': random.randint(1, max_autoshop_id),
            'supplier_id': random.randint(1, max_supplier_id),
            'required_cars_bought_amount': random.randint(5, 50),
            'increasing_percent_per_requirements_fulfilled': round(random.uniform(0.5, 5), 2)
        })
    return autoshop_discounts


if __name__ == '__main__':
    added_cars = generate_cars(COUNT)
    added_users = generate_users(COUNT)
    added_general_discounts = generate_general_discounts(COUNT)
    added_suppliers = generate_suppliers(COUNT, COUNT)
    added_autoshops = generate_autoshops(COUNT, COUNT)
    car_discounts = generate_car_discounts(COUNT, COUNT)
    added_user_personal_discounts = generate_user_personal_discounts(COUNT, COUNT, COUNT)
    added_autoshop_personal_discounts = generate_autoshop_personal_discounts(COUNT, COUNT, COUNT)

    write_to_file('cars', 'cars.json', added_cars)
    write_to_file('users', 'users.json', added_users)
    write_to_file('discounts', 'general_discounts.json', added_general_discounts)
    write_to_file('suppliers', 'suppliers.json', added_suppliers)
    write_to_file('autoshops', 'autoshops.json', added_autoshops)
    write_to_file('discounts', 'car_discounts.json', car_discounts)
    write_to_file('discounts', 'user_personal_discounts.json', added_user_personal_discounts)
    write_to_file('discounts', 'autoshop_personal_discounts.json', added_autoshop_personal_discounts)

    print(f"Генерация завершена. Созданы файлы с {COUNT} записями для каждой модели.")
