import enum

from django.contrib.auth.base_user import BaseUserManager

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

    def create_superuser(self, username, email, telephone='', age=18, balance=0, role=None, password=None):
        user = self.create_user(username, email, telephone, age, balance, role=role, password=password)
        user.role = UserRole.Admin
        user.is_staff = True
        user.save()

        return user