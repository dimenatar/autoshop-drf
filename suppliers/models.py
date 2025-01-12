from django.db import models

from cars.models import Car
from discounts.models import CarDiscount, GeneralDiscount


class Supplier(models.Model):
    name = models.TextField(blank=True, null=True)
    cars = models.ManyToManyField(Car)
    car_discounts = models.ManyToManyField(CarDiscount)
    general_discount_id = models.ForeignKey(GeneralDiscount, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f"name: {self.name}, cars: {self.cars}, car discounts: {self.car_discounts}, general discount id: {self.general_discount_id}"
