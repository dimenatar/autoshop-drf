import pytest
from django.contrib.auth import authenticate

from users.serializers import (
    CustomRegisterSerializer,
    CustomLoginSerializer,
    UserSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from users.models import UserRole


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(transactional_db):
    pass


class TestCustomRegisterSerializer:

    def test_valid_registration_data(self, user_data):
        serializer = CustomRegisterSerializer(data=user_data)
        assert serializer.is_valid()

    def test_missing_required_fields(self, user_data):
        del user_data['username']
        serializer = CustomRegisterSerializer(data=user_data)
        assert not serializer.is_valid()
        assert 'username' in serializer.errors

    def test_password_mismatch(self, user_data):
        user_data['password2'] = 'differentpassword'
        serializer = CustomRegisterSerializer(data=user_data)
        assert not serializer.is_valid()

    def test_email_already_exists(self, user_data, existing_user):
        user_data['email'] = existing_user.email
        serializer = CustomRegisterSerializer(data=user_data)

        assert not serializer.is_valid()
        assert 'email' in serializer.errors

    def test_invalid_email_format(self, user_data):
        user_data['email'] = 'invalid-email'
        serializer = CustomRegisterSerializer(data=user_data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors

    def test_age_validation(self, user_data):
        user_data['age'] = 0
        serializer = CustomRegisterSerializer(data=user_data)
        assert not serializer.is_valid()
        assert 'age' in serializer.errors

    def test_default_role_assignment(self, user_data):
        del user_data['role']
        serializer = CustomRegisterSerializer(data=user_data)
        assert serializer.is_valid()
        assert serializer.validated_data['role'] == UserRole.Customer.value


class TestCustomLoginSerializer:

    def test_valid_login_data(self, existing_user):
        existing_user.is_email_verified = True
        existing_user.save()

        login_data = {
            "email": existing_user.email,
            "password": "existingpassword123"
        }

        user = authenticate(username=existing_user.email, password=login_data['password'])
        assert user is not None, "User should be authenticated"
        assert user == existing_user, "Authenticated user should match existing_user"

        serializer = CustomLoginSerializer(data=login_data)
        assert serializer.is_valid(), f"Serializer should be valid, but got errors: {serializer.errors}"
        assert 'user' in serializer.validated_data
        assert serializer.validated_data['user'] == existing_user

    def test_invalid_credentials(self, login_data):
        serializer = CustomLoginSerializer(data=login_data)
        assert not serializer.is_valid()

    def test_unverified_email(self, login_data, existing_user):
        existing_user.is_email_verified = False
        existing_user.save()

        serializer = CustomLoginSerializer(data=login_data)
        assert not serializer.is_valid()

    def test_inactive_user(self, login_data, existing_user):
        existing_user.is_active = False
        existing_user.is_email_verified = True
        existing_user.save()

        serializer = CustomLoginSerializer(data=login_data)
        assert not serializer.is_valid()


class TestUserSerializer:

    def test_user_serialization(self, existing_user):
        serializer = UserSerializer(existing_user)
        data = serializer.data

        assert data['username'] == existing_user.username
        assert data['email'] == existing_user.email
        assert data['age'] == existing_user.age
        assert data['telephone'] == existing_user.telephone
        assert data['balance'] == existing_user.balance
        assert data['role'] == existing_user.role
        assert 'is_email_verified' in data

    def test_user_deserialization(self, existing_user):
        update_data = {
            "username": "updateduser",
            "age": 35,
            "telephone": "+0987654321"
        }

        serializer = UserSerializer(
            instance=existing_user,
            data=update_data,
            partial=True
        )
        assert serializer.is_valid()
        updated_user = serializer.save()

        assert updated_user.username == "updateduser"
        assert updated_user.age == 35
        assert updated_user.telephone == "+0987654321"

    def test_password_update(self, existing_user):
        new_password = "newpassword123"
        update_data = {
            "password": new_password
        }

        serializer = UserSerializer(
            instance=existing_user,
            data=update_data,
            partial=True
        )
        assert serializer.is_valid()
        updated_user = serializer.save()

        assert updated_user.check_password(new_password)


class TestPasswordResetSerializers:

    def test_password_reset_request_valid_email(self):
        serializer = PasswordResetRequestSerializer(data={
            "email": "test@example.com"
        })
        assert serializer.is_valid()

    def test_password_reset_request_invalid_email(self):
        serializer = PasswordResetRequestSerializer(data={
            "email": "invalid-email"
        })
        assert not serializer.is_valid()
        assert 'email' in serializer.errors

    def test_password_reset_confirm_valid_data(self):
        serializer = PasswordResetConfirmSerializer(data={
            "token": "123e4567-e89b-12d3-a456-426614174000",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        })
        assert serializer.is_valid()

    def test_password_reset_confirm_password_mismatch(self):
        serializer = PasswordResetConfirmSerializer(data={
            "token": "123e4567-e89b-12d3-a456-426614174000",
            "new_password": "newpassword123",
            "confirm_password": "differentpassword"
        })
        assert not serializer.is_valid()

    def test_password_reset_confirm_weak_password(self):
        serializer = PasswordResetConfirmSerializer(data={
            "token": "123e4567-e89b-12d3-a456-426614174000",
            "new_password": "123",
            "confirm_password": "123"
        })
        assert not serializer.is_valid()
        assert 'new_password' in serializer.errors
