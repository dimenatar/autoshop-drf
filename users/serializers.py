from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User
from users.user_manager import UserRole


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


class RegistrationSerializer(BaseValidatedSerializer):
    password = serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

class LoginSerializer(BaseValidatedSerializer):

    def validate(self, data: dict) -> dict:
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )


        return super().validate(data) # type: ignore

class UserSerializer(BaseValidatedSerializer):
    class Meta:
        model = User
        fields = '__all__'