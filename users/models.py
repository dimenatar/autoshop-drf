import enum

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.models import BaseModel

ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Customer', 'Customer'),
)

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)]) #sorry drandma
    telephone = models.CharField(max_length=13)
    balance = models.FloatField(validators=[MinValueValidator(0)])
    role = models.CharField(choices=ROLE_CHOICES)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    is_staff = True

    def __str__(self) -> str:
        return f"name: {self.username}, role: {self.role} email: {self.email}"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



class UserRole(enum.Enum):
    ADMIN = 'Admin'
    CUSTOMER = 'Customer'

