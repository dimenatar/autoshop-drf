from django.core.validators import MinValueValidator
from django.db import models
from django_countries.fields import CountryField
from available_cars.models import AvailableCars
from cars.models import CarDetails
from discounts.models import CarDiscount
from users.models import User


class AutoShop(CarDetails):
    name = models.CharField(max_length=100)
    location = CountryField()
    balance = models.FloatField(validators=[MinValueValidator(0.0)])
    cars_in_stock = models.ManyToManyField(AvailableCars)
    car_discounts = models.ManyToManyField(CarDiscount)
    general_discount_id = models.ForeignKey('discounts.GeneralDiscount',
                                            on_delete=models.CASCADE, null=True)
    buyers = models.ManyToManyField(User)

    def __str__(self) -> str:
        return f"{super().__str__()}, name: {self.name}, balance: {self.balance}"
