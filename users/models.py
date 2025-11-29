import enum

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import BaseModel

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('customer', 'Customer'),
)


class User(BaseModel):
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    telephone = models.CharField(max_length=13)
    balance = models.FloatField(validators=[MinValueValidator(0)])
    role = models.CharField(choices=ROLE_CHOICES)
    password = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self) -> str:
        return f"name: {self.name}, role: {self.role} email: {self.email}"

    def purchase_car(self, price: float) -> None:
        self.balance -= price
        self.save()


class UserRole(enum.Enum):
    ADMIN = 'Admin'
    CUSTOMER = 'Customer'
