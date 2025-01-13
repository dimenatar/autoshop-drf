from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.models import BaseModel


class BaseDiscount(BaseModel):
    percent = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f'percent: {self.percent}%'

    class Meta:
        abstract = True

class GeneralDiscount(BaseDiscount):
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"name: {self.name} {super()} dates:{self.start_date}/{self.end_date}, description: {self.description}"

class UserPersonalDiscount(BaseDiscount):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    autoshop_id = models.ForeignKey('autoshops.AutoShop', on_delete=models.CASCADE, default=0, null=True)

    def __str__(self):
        return f"user:{self.user} {super()}"

class CarDiscount(BaseDiscount):
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE)

    def __str__(self):
        return f"car:{self.car} {super()}"