from typing import Any

from rest_framework.request import Request

from users.serializers import UserSerializer, LoginSerializer


class UserService:

    def __init__(self) -> None:
        self.user_serializer = UserSerializer
        self.serializer_class = LoginSerializer

    def get_user_data(self, request: Request) -> Any:
        serializer = self.user_serializer(request.user)

        return serializer.data

    def update_user_data(self, request: Request) -> Any:
        serializer_data = request.data.get('user', {})
        serializer = self.user_serializer(
            request.user,
            data=serializer_data,
            partial=True
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
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return serializer.data


user_service = UserService()