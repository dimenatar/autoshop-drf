from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from cars.models import Car
from users.models import User


class Discount(models.Model):
    percent = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f'percent: {self.percent}%'

    class Meta:
        abstract = True

class GeneralDiscount(Discount):
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"name: {self.name} {super()} dates:{self.start_date}/{self.end_date}, description: {self.description}"

class UserPersonalDiscount(Discount):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"user:{self.user} {super()}"

class CarDiscount(Discount):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"car:{self.car} {super()}"