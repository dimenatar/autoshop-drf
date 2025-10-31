import enum

from django.contrib.auth.base_user import BaseUserManager
from users.models import User

ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Customer', 'Customer'),
)

class UserRole(enum.IntEnum):
    Admin = 0
    Customer = 1

class UserManager(BaseUserManager):
    def create_user(self, username: str, email: str, telephone: str, age: int, balance: float, role:UserRole=UserRole.Customer, password:str='') -> User:
        role = role or UserRole.Customer
        user: User = self.model(username=username, email=self.normalize_email(email), role=role, telephone=telephone, age=age, balance=balance)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username: str, email: str, telephone: str='', age: int=18, balance: float=0, role:UserRole=UserRole.Customer, password: str='') -> User:
        user = self.create_user(username, email, telephone, age, balance, role=role, password=password)
        user.role = UserRole.Admin
        user.is_staff = True
        user.save()

        return user