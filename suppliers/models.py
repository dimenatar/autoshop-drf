from django.db import models
from available_cars.models import AvailableCars
from core.models import BaseModel
from discounts.models import CarDiscount

class Supplier(BaseModel):
    name = models.TextField(blank=True, null=True)
    cars_in_stock = models.ManyToManyField(AvailableCars)
    car_discounts = models.ManyToManyField(CarDiscount)
    general_discount_id = models.ForeignKey('discounts.GeneralDiscount',
                                            on_delete=models.CASCADE, null = True)

    def __str__(self):
        return (f"name: {self.name}"
                f"general discount id: {self.general_discount_id}")
