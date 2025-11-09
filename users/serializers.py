from typing import Dict, Any

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth import authenticate
from django.http import HttpRequest

from core.configs.django_config import DjangoConfig
from dj_rest_auth.serializers import PasswordResetSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import UserRole
from dj_rest_auth.serializers import LoginSerializer as BaseLoginSerializer

User = get_user_model()


class BaseValidatedSerializer(serializers.Serializer):

    password = serializers.CharField()
    age = serializers.IntegerField()
    telephone = serializers.CharField()
    role = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()
    balance = serializers.FloatField()

    @staticmethod
    def validate_required_attr(data: str) -> str:
        if data is None:
            raise serializers.ValidationError(f"{data=}".split('=')[0] + " is required")
        return data

    def validate_email(self, email: str) -> str:
        return self.validate_required_attr(email)

    def validate_password(self, password: str) -> str:
        return self.validate_required_attr(password)

    def validate_telephone(self, telephone: str) -> str:
        return self.validate_required_attr(telephone)

    def validate_username(self, username: str) -> str:
        return self.validate_required_attr(username)

    @staticmethod
    def validate_balance(balance: float) -> float:
        if balance is None:
            balance = 0
        return balance

    @staticmethod
    def validate_age(age: int) -> int:
        if age is None:
            age = 18
        return age

    @staticmethod
    def validate_role(role: UserRole) -> UserRole:
        if role is None:
            role = UserRole.Customer
        return role


class UserSerializer(BaseValidatedSerializer):
    is_email_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'age', 'telephone', 'balance', 'role', 'is_email_verified']
        read_only_fields = ['id', 'is_email_verified']

    def update(self, instance: Any, validated_data: Dict[str, Any]) -> Any:
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True, min_value=1, max_value=100)
    telephone = serializers.CharField(required=True, max_length=13)
    balance = serializers.FloatField(required=False, default=0, min_value=0)
    role = serializers.ChoiceField(
        choices=[(role.value, role.value) for role in UserRole],
        required=False,
        default=UserRole.Customer.value
    )

    def get_cleaned_data(self) -> Any:
        data = super().get_cleaned_data()
        data.update({
            'username': self.validated_data.get('username', ''),
            'age': self.validated_data.get('age', 18),
            'telephone': self.validated_data.get('telephone', ''),
            'balance': self.validated_data.get('balance', 0),
            'role': self.validated_data.get('role', UserRole.Customer.value),
        })
        return data

    def validate_email(self, email: str) -> str:
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return email

    def save(self, request: HttpRequest) -> Any:
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        user.username = self.cleaned_data['username']
        user.age = self.cleaned_data['age']
        user.telephone = self.cleaned_data['telephone']
        user.balance = self.cleaned_data['balance']
        user.role = self.cleaned_data['role']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.is_email_verified = False
        user.save()

        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class CustomLoginSerializer(BaseLoginSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def get_cleaned_data(self) -> Dict[str, str]:
        return {
            'email': self.validated_data.get('email', ''),
            'password': self.validated_data.get('password', ''),
        }

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        if not user.is_email_verified:
            raise serializers.ValidationError(
                'Please verify your email address before logging in.'
            )

        attrs['user'] = user
        return attrs


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.UUIDField()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(min_length=6)
    confirm_password = serializers.CharField(min_length=6)

    def validate(self, data: Dict[str, Any]) -> Any:
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self) -> Dict[str, Any]:
        link = DjangoConfig.BASE_URL
        return {
            'email_template_name': 'registration/password_reset_email.html',
            'html_email_template_name': 'registration/password_reset_email.html',
            'subject_template_name': 'registration/password_reset_subject.txt',
            'extra_email_context': {
                'frontend_url': str(link),
            }
        }
