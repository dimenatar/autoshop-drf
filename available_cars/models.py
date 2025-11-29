from django.core.validators import MinValueValidator
from django.db import models

from core.models import BaseModel


class AvailableCars(BaseModel):
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.FloatField()
    last_purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Available Cars"

    def __str__(self) -> str:
        return f'car: {self.car}, amount: {self.amount}'
