import enum

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.models import BaseModel

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('customer', 'Customer'),
)

class User(BaseModel):#, AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)]) #sorry drandma
    telephone = models.CharField(max_length=13)
    balance = models.FloatField(validators=[MinValueValidator(0)])
    role = models.CharField(choices = ROLE_CHOICES)
    password = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"name: {self.name}, age: {self.age}, telephone: {self.telephone}, balance: {self.balance}, role: {self.role}, password: {self.password}, email: {self.email}"

class UserRole(enum.Enum):
    Admin = 0
    Customer = 1

# class UserManager(BaseUserManager):
#     def create_user(self, name, age, telephone, balance, role, password, email):
#         user = self.model(name = name, age = age, telephone = telephone, balance = balance, role = role, email = email)
#         user.set_password(password)
#         user.save(using = self._db)
#
#         return user
