from django.core.validators import MinValueValidator
from django.db import models
from django_countries.fields import CountryField

from available_cars.models import AvailableCars
from cars.models import Car, CarDetails
from core.configs.celery_config import CeleryConfig
from discounts.models import CarDiscount
from users.models import User


class AutoShop(CarDetails):
    name = models.CharField(max_length=100)
    location = CountryField()
    balance = models.FloatField(validators=[MinValueValidator(0.0)])
    cars_in_stock = models.ManyToManyField(AvailableCars)
    car_discounts = models.ManyToManyField(CarDiscount)
    general_discount = models.ForeignKey('discounts.GeneralDiscount',
                                         on_delete=models.CASCADE, null=True)
    buyers = models.ManyToManyField(User)

    def __str__(self) -> str:
        return f"{super().__str__()}, name: {self.name}, balance: {self.balance}"

    def purchase_car(self, car: Car, price: float) -> None:
        found_cars = list(self.cars_in_stock.filter(car=car))
        found_car = None
        if found_cars:
            found_car = found_cars[0]
        else:
            found_car = AvailableCars.objects.create(
                car=car,
                amount=0,
                price=CeleryConfig.get_random_car_price()
            )
            found_car.save()
            self.cars_in_stock.add(found_car)
        found_car.amount += 1
        found_car.save()
        self.balance -= price
        self.save()

    def try_add_buyer(self, user: User) -> bool:
        if not self.buyers.filter(email=user.email).exists():
            self.buyers.add(user)
            return True
        return False

    def reduce_car_amount(self, available_car: AvailableCars) -> None:
        for car in self.cars_in_stock.filter(is_active=True, car=available_car.car).all():
            car.amount -= 1
            if car.amount == 0:
                car.is_active = False
            car.save()
