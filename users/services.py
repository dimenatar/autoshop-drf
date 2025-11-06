from typing import Dict, Any
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.request import Request
from core.configs.django_config import DjangoConfig
from users.models import User, EmailVerificationToken, PasswordResetToken
from users.serializers import UserSerializer, CustomRegisterSerializer, CustomLoginSerializer


class UserService:

    def __init__(self):
        self.user_serializer = UserSerializer
        self.register_serializer = CustomRegisterSerializer
        self.login_serializer = CustomLoginSerializer

    def get_user_data(self, request: Request) -> Dict[str, Any]:
        serializer = self.user_serializer(request.user)
        return serializer.data

    def update_user_data(self, request: Request) -> Dict[str, Any]:
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

    def login_user(self, request: Request) -> Dict[str, Any]:
        user_data = request.data.get('user', {})

        serializer = self.login_serializer(
            data=user_data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user_serializer = self.user_serializer(user)

        return user_serializer.data

    def register_user(self, request: Request) -> Dict[str, Any]:
        user_data = request.data.get('user', {})

        serializer = self.register_serializer(
            data=user_data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save(request)

        self._send_verification_email(user)

        user_serializer = self.user_serializer(user)
        return user_serializer.data

    @staticmethod
    def _send_verification_email(user: User) -> None:
        verification_token = EmailVerificationToken.objects.create(user=user)

        verification_url = f"http://localhost:8000/api/users/verify-email/{verification_token.token}/"
        subject = 'Verify your email address'
        message = f'''
        Hello {user.username},

        Please verify your email address by clicking the link below:
        {verification_url}

        Thank you!
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

    @staticmethod
    def verify_email(token: str) -> bool:
        try:
            verification_token = EmailVerificationToken.objects.get(
                token=token,
                is_used=False
            )
            user = verification_token.user
            user.is_email_verified = True
            user.save()

            verification_token.is_used = True
            verification_token.save()

            return True
        except EmailVerificationToken.DoesNotExist:
            return False

    def request_password_reset(self, email: str) -> bool:
        try:
            user = User.objects.get(email=email)
            reset_token = PasswordResetToken.objects.create(user=user)
            self._send_password_reset_email(user, reset_token.token)
            return True
        except User.DoesNotExist:
            return True

    @staticmethod
    def reset_password(token: str, new_password: str) -> bool:
        try:
            reset_token = PasswordResetToken.objects.get(
                token=token,
                is_used=False
            )
            user = reset_token.user
            user.set_password(new_password)
            user.save()

            reset_token.is_used = True
            reset_token.save()

            return True
        except PasswordResetToken.DoesNotExist:
            return False

    @staticmethod
    def _send_password_reset_email(user: User, token: str) -> None:
        reset_url = f"{DjangoConfig.BASE_URL}/api/users/reset-password/{token}/"
        subject = 'Password Reset Request'
        message = f'''
        Hello {user.username},

        You requested a password reset. Click the link below to reset your password:
        {reset_url}

        If you didn't request this, please ignore this email.

        Thank you!
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )


user_service = UserService()