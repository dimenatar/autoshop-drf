import pytest
from unittest.mock import patch, MagicMock

from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from allauth.account.models import EmailConfirmation

from users.models import UserRole

User = get_user_model()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(transactional_db):
    pass


class TestUserService:

    @patch('users.services.UserSerializer')
    @patch('users.services.CustomRegisterSerializer')
    def test_register_user_success(self, mock_register_serializer, mock_user_serializer, user_service, mock_request):
        mock_user = MagicMock()
        mock_user.username = 'testuser'
        mock_user.email = 'test@example.com'
        mock_user.age = 25
        mock_user.telephone = '+1234567890'
        mock_user.balance = 100.0
        mock_user.role = UserRole.Customer.value
        mock_user.is_email_verified = False

        mock_register_instance = MagicMock()
        mock_register_instance.is_valid.return_value = True
        mock_register_instance.save.return_value = mock_user
        mock_register_serializer.return_value = mock_register_instance

        expected_user_data = {
            'username': 'testuser', 'email': 'test@example.com',
            'age': 25, 'telephone': '+1234567890', 'balance': 100.0,
            'role': UserRole.Customer.value, 'is_email_verified': False
        }
        mock_user_serializer.return_value.data = expected_user_data

        result = user_service.register_user(mock_request)
        expected_user_data['password'] = result['password']

        assert result == expected_user_data

    def test_register_user_validation_error(self, user_service, mock_request):
        mock_request.data['user']['email'] = "invalid-email"

        with pytest.raises(ValidationError):
            user_service.register_user(mock_request)

    @patch('users.services.UserSerializer')
    @patch('users.services.CustomLoginSerializer')
    def test_login_user_success(self, mock_login_serializer, mock_user_serializer, user_service, mock_request):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            telephone="+1234567890",
            age=25,
            balance=100.0,
            role=UserRole.Customer.value,
            password="testpassword123"
        )
        user.is_email_verified = True
        user.save()

        mock_login_instance = MagicMock()
        mock_login_instance.is_valid.return_value = True
        mock_login_instance.validated_data = {'user': user}
        mock_login_serializer.return_value = mock_login_instance

        expected_user_data = {
            'username': user.username,
            'email': user.email,
            'age': user.age,
            'telephone': user.telephone,
            'balance': user.balance,
            'role': user.role,
            'is_email_verified': user.is_email_verified
        }
        mock_user_serializer.return_value.data = expected_user_data

        mock_request.data = {
            'user': {
                "email": "test@example.com",
                "password": "testpassword123"
            }
        }

        result = user_service.login_user(mock_request)

        expected_user_data['password'] = result['password']
        assert result == expected_user_data

    def test_get_user_data(self, user_service, verified_user, mock_request):
        mock_request.user = verified_user

        result = user_service.get_user_data(mock_request)

        assert 'username' in result
        assert result['username'] == verified_user.username
        assert result['email'] == verified_user.email

    def test_update_user_data(self, user_service, verified_user, mock_request):
        mock_request.user = verified_user
        mock_request.data = {
            'user': {
                "username": "updateduser",
                "age": 35
            }
        }

        result = user_service.update_user_data(mock_request)

        assert result['username'] == "updateduser"
        assert result['age'] == 35
        verified_user.refresh_from_db()
        assert verified_user.username == "updateduser"
        assert verified_user.age == 35

    def test_update_user_data_with_password(self, user_service, verified_user, mock_request):
        mock_request.user = verified_user
        new_password = "newpassword123"
        mock_request.data = {
            'user': {
                "password": new_password
            }
        }

        user_service.update_user_data(mock_request)

        verified_user.refresh_from_db()
        assert verified_user.check_password(new_password)

    def test_verify_email_success(self, user_service, user_with_email_confirmation):
        from unittest.mock import MagicMock
        user, email_address, confirmation = user_with_email_confirmation

        mock_request = MagicMock()

        mock_request.sent = timezone.now()
        result = user_service.verify_email(mock_request, confirmation.key)

        assert result is True

        email_address.refresh_from_db()
        assert email_address.verified is True

    @patch('allauth.account.models.EmailConfirmation')
    def test_verify_email_invalid_token(self, mock_email_confirmation, user_service):
        mock_email_confirmation.DoesNotExist = EmailConfirmation.DoesNotExist
        mock_email_confirmation.objects.get.side_effect = EmailConfirmation.DoesNotExist

        result = user_service.verify_email(MagicMock(), "invalid-key")

        assert result is False

    @patch('allauth.account.forms.ResetPasswordForm')
    def test_request_password_reset_success(self, mock_form_class, user_service, db):
        mock_form = MagicMock()
        mock_form.is_valid.return_value = True
        mock_form_class.return_value = mock_form

        result = user_service.request_password_reset("test@example.com")

        assert result is True
        mock_form.save.assert_called_once()
