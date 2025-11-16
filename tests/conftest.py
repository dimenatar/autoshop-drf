import os
from unittest.mock import MagicMock

import django
import pytest
from allauth.account.models import EmailAddress, EmailConfirmation
from django.conf import settings
from django.utils import timezone

from users.models import UserRole, User
from users.services import UserService

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

if not settings.configured:
    django.setup()

@pytest.fixture
def user_with_unverified_email(db):
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        telephone="+1234567890",
        age=25,
        balance=100.0,
        role=UserRole.Customer.value,
        password="testpassword123"
    )

    email_address = EmailAddress.objects.create(
        user=user,
        email=user.email,
        primary=True,
        verified=False
    )

    confirmation = EmailConfirmation.create(email_address)
    confirmation.sent = timezone.now()
    confirmation.save()

    return user, email_address


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(transactional_db):
    pass


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password1": "testpassword123",
        "password2": "testpassword123",
        "telephone": "+1234567890",
        "age": 25,
        "balance": 100.0,
        "role": UserRole.Customer.value
    }


@pytest.fixture
def login_data():
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }


@pytest.fixture
def existing_user(db):
    user = User.objects.create_user(
        username="existinguser",
        email="existing@example.com",
        telephone="+1234567890",
        age=30,
        balance=50.0,
        role=UserRole.Customer.value,
        password="existingpassword123"
    )

    EmailAddress.objects.create(
        user=user,
        email=user.email,
        primary=True,
        verified=False
    )

    return user


@pytest.fixture
def user_service():
    return UserService()


@pytest.fixture
def user_with_email_confirmation(db):
    user = User.objects.create_user(
        username="confirmation_user",
        email="confirmation@example.com",
        telephone="+1234567890",
        age=25,
        balance=100.0,
        role=UserRole.Customer.value,
        password="testpassword123"
    )

    email_address = EmailAddress.objects.create(
        user=user,
        email=user.email,
        primary=True,
        verified=False
    )
    confirmation = EmailConfirmation.create(email_address)
    return user, email_address, confirmation


@pytest.fixture
def mock_request():
    request = MagicMock()
    request.data = {
        'user': {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "telephone": "+1234567890",
            "age": 25,
            "balance": 100.0,
            "role": UserRole.Customer.value
        }
    }
    return request


@pytest.fixture
def verified_user(db):
    user = User.objects.create_user(
        username="verifieduser",
        email="verified@example.com",
        telephone="+1234567890",
        age=30,
        balance=50.0,
        role=UserRole.Customer.value,
        password="password123"
    )

    EmailAddress.objects.create(
        user=user,
        email=user.email,
        primary=True,
        verified=True
    )

    return user


@pytest.fixture
def user_with_verified_email(db):
    user = User.objects.create_user(
        username="verifieduser2",
        email="verified2@example.com",
        telephone="+1234567891",
        age=35,
        balance=75.0,
        role=UserRole.Customer.value,
        password="password123"
    )

    EmailAddress.objects.create(
        user=user,
        email=user.email,
        primary=True,
        verified=True
    )

    return user


@pytest.fixture
def admin_user(db):
    user = User.objects.create_user(
        username="adminuser",
        email="admin@example.com",
        telephone="+1234567892",
        age=40,
        balance=1000.0,
        role=UserRole.Admin.value,
        password="adminpassword123"
    )

    EmailAddress.objects.create(
        user=user,
        email=user.email,
        primary=True,
        verified=True
    )

    return user


@pytest.fixture
def multiple_users(db):
    users = []
    for i in range(3):
        user = User.objects.create_user(
            username=f"user{i}",
            email=f"user{i}@example.com",
            telephone=f"+123456789{i}",
            age=25 + i,
            balance=100.0 * i,
            role=UserRole.Customer.value,
            password=f"password{i}123"
        )

        EmailAddress.objects.create(
            user=user,
            email=user.email,
            primary=True,
            verified=(i % 2 == 0)
        )

        users.append(user)

    return users
