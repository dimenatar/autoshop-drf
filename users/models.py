import enum

from datetime import datetime, timedelta
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import BaseModel

ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Customer', 'Customer'),
)

class UserRole(enum.IntEnum):
    Admin = 0
    Customer = 1

class UserManager(BaseUserManager):
    def create_user(self, username, email, telephone, age, balance, role=None, password=None):
        role = role or UserRole.Customer
        user = self.model(username=username, email=self.normalize_email(email), role=role, telephone=telephone, age=age, balance=balance)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, telephone, age, balance, role=None, password=None):
        user = self.create_user(username, email, telephone, age, balance, role=role, password=password)
        user.role = UserRole.Admin
        user.is_staff = True
        user.save()

        return user

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)]) #sorry drandma
    telephone = models.CharField(max_length=13)
    balance = models.FloatField(validators=[MinValueValidator(0)])
    role = models.CharField(choices = ROLE_CHOICES)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{super().__str__()} name: {self.username}, age: {self.age}, telephone: {self.telephone}, balance: {self.balance}, role: {self.role}, password: {self.password}, email: {self.email}"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username