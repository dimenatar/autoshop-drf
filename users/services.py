from typing import Any

from allauth.account.internal.flows.email_verification import send_verification_email_to_address
from allauth.account.models import EmailConfirmation, EmailAddress
from django.http import HttpRequest
from django.utils import timezone
from rest_framework.request import Request

from users.models import User
from users.serializers import UserSerializer, CustomRegisterSerializer, CustomLoginSerializer


class UserService:

    def __init__(self) -> None:
        self.user_serializer = UserSerializer
        self.register_serializer = CustomRegisterSerializer
        self.login_serializer = CustomLoginSerializer

    def get_user_data(self, request: Request) -> Any:
        serializer = self.user_serializer(request.user)
        return serializer.data

    def update_user_data(self, request: Request) -> Any:
        serializer_data = request.data.get('user', {})

        serializer = self.user_serializer(
            request.user,
            data=serializer_data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(request.user, key, value)

        if password is not None:
            request.user.set_password(password)

        request.user.save()

        return self.user_serializer(request.user).data

    def login_user(self, request: Request) -> Any:
        user_data = request.data.get('user', {})

        serializer = self.login_serializer(
            data=user_data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user_serializer = self.user_serializer(user)

        return user_serializer.data

    def register_user(self, request: Request) -> Any:
        user_data = request.data.get('user', {})

        serializer = self.register_serializer(
            data=user_data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save(request)

        self._send_email_confirmation(request._request, user)

        user_serializer = self.user_serializer(user)
        return user_serializer.data

    def _send_email_confirmation(self, request: HttpRequest, user: User) -> None:
        try:
            email = EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
                defaults={'primary': True, 'verified': False}
            )
            send_verification_email_to_address(request, email[0])

        except Exception as e:
            print(f"Failed to send email confirmation: {e}")

    @staticmethod
    def verify_email(request: Request, key: str) -> bool:
        try:
            confirmation = EmailConfirmation.objects.get(key=key)
            confirmation.sent = timezone.now()
            confirmation.confirm(request)
            return True
        except EmailConfirmation.DoesNotExist:
            return False

    @staticmethod
    def request_password_reset(email: str) -> bool:
        from allauth.account.forms import ResetPasswordForm

        form = ResetPasswordForm(data={'email': email})
        if form.is_valid():
            form.save(request=None)
            return True
        return False

    def reset_password(self, token: str, new_password: str) -> bool:
        try:
            from allauth.account.models import EmailConfirmation
            confirmation = EmailConfirmation.objects.get(key=token, is_used=False)

            user = confirmation.email_address.user
            user.set_password(new_password)
            user.save()

            confirmation.is_used = True
            confirmation.save()

            return True

        except EmailConfirmation.DoesNotExist:
            try:
                return self._reset_password_alternative(token, new_password)
            except Exception:
                return False

    def _reset_password_alternative(self, token: str, new_password: str) -> bool:
        try:
            from allauth.account.models import EmailConfirmation
            confirmation = EmailConfirmation.objects.get(key=token, is_used=False)
            user = confirmation.email_address.user

            user.set_password(new_password)
            user.save()

            confirmation.is_used = True
            confirmation.save()

            return True
        except Exception:
            return False


user_service = UserService()
