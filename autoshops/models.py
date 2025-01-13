from django.core.validators import MinValueValidator
from django.db import models

from available_cars.models import AvailableCars
from core.models import BaseModel
from discounts.models import CarDiscount
from users.models import User



class AutoShop(BaseModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    balance = models.FloatField(validators=[MinValueValidator(0.0)] )
    cars_in_stock = models.ManyToManyField(AvailableCars)
    car_discounts = models.ManyToManyField(CarDiscount)
    general_discount_id = models.ForeignKey('discounts.GeneralDiscount', on_delete=models.CASCADE, null = True)
    buyers = models.ManyToManyField(User)

    def __str__(self):
        return f"name: {self.name}, location: {self.location}, balance: {self.balance}, available_cars: {self.cars_in_stock}, discounts: {self.car_discounts}, general_discount {self.general_discount_id}"