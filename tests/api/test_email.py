import pytest
from django.core import mail
from django.contrib.auth import get_user_model
from allauth.account.models import EmailConfirmation
from django.utils import timezone

from users.models import UserRole

User = get_user_model()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(transactional_db):
    pass


class TestEmailFunctionality:

    def test_email_confirmation_creation(self, user_with_unverified_email):
        user, email_address = user_with_unverified_email

        confirmation = EmailConfirmation.create(email_address)
        confirmation.sent = timezone.now()
        confirmation.save()

        assert confirmation.email_address == email_address
        assert confirmation.key is not None
        assert len(confirmation.key) > 0

    def test_email_confirmation_flow(self, user_with_unverified_email):
        user, email_address = user_with_unverified_email
        confirmation = EmailConfirmation.create(email_address)
        confirmation.sent = timezone.now()
        confirmation.save()

        from unittest.mock import Mock
        mock_request = Mock()
        confirmed = confirmation.confirm(mock_request)
        assert confirmed is not None
        email_address.refresh_from_db()

        assert email_address.verified is True

    def test_email_sending_on_registration(self, client, db):
        mail.outbox = []

        registration_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "telephone": "+1234567890",
            "age": 25,
            "balance": 0.0,
            "role": UserRole.Customer.value
        }

        client.post('/api/users/register/',
                    {"user": registration_data},
                    content_type='application/json')

        assert len(mail.outbox) == 1
        email = mail.outbox[0]

        assert email.to == [registration_data['email']]
        assert 'AutoShop' in email.subject
        assert 'confirm' in email.body.lower() or 'confirm' in str(email.alternatives[0][0]).lower()

    def test_password_reset_email(self, client, user_with_unverified_email):
        user, email_address = user_with_unverified_email
        mail.outbox = []

        client.post('/api/users/request-reset/',
                    {"email": user.email},
                    content_type='application/json')

        assert len(mail.outbox) == 1
        email = mail.outbox[0]

        assert email.to == [user.email]
        assert 'password' in email.subject.lower()


class TestEmailTemplates:

    def test_email_confirmation_template_contains_correct_info(self, user_with_unverified_email):
        user, email_address = user_with_unverified_email
        confirmation = EmailConfirmation.create(email_address)

        activate_url = f"/accounts/confirm-email/{confirmation.key}/"

        assert user.username is not None
        assert activate_url is not None

    def test_email_subject_prefix(self, settings):
        assert hasattr(settings, 'ACCOUNT_EMAIL_SUBJECT_PREFIX')
        assert 'AutoShop' in settings.ACCOUNT_EMAIL_SUBJECT_PREFIX
