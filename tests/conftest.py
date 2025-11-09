from unittest.mock import MagicMock

import pytest
from allauth.account.models import EmailAddress, EmailConfirmation
from django.utils import timezone

from users.models import UserRole, User
from users.services import UserService


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
    return User.objects.create_user(
        username="existinguser",
        email="existing@example.com",
        telephone="+1234567890",
        age=30,
        balance=50.0,
        role=UserRole.Customer.value,
        password="existingpassword123"
    )


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
    user.is_email_verified = True
    user.save()
    return user
