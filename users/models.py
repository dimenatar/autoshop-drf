import enum

from datetime import datetime, timedelta

import jwt

from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.models import BaseModel

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('customer', 'Customer'),
)




class UserRole(enum.Enum):
    Admin = 0
    Customer = 1

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        user = self.model(username=username, email=self.normalize_email(email), role=UserRole.Customer)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.role = UserRole.Admin
        user.is_staff = True
        user.save()

        return user

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)]) #sorry drandma
    telephone = models.CharField(max_length=13)
    balance = models.FloatField(validators=[MinValueValidator(0)])
    role = models.CharField(choices = ROLE_CHOICES)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{super().__str__()} name: {self.name}, age: {self.age}, telephone: {self.telephone}, balance: {self.balance}, role: {self.role}, password: {self.password}, email: {self.email}"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')