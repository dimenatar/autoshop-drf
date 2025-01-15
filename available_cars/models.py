from django.core.validators import MinValueValidator
from django.db import models

from core.models import BaseModel


# Create your models here.
class AvailableCars(BaseModel):
    car_id = models.ForeignKey('cars.Car', on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.FloatField()

    class Meta:
        verbose_name_plural = "Available Cars"

    def __str__(self):
        return f'{super().__str__()}, car: {self.car_id}, amount: {self.amount}, price: {self.price}'