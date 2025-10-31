from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .renderers import UserJSONRenderer

from .serializers import LoginSerializer, RegistrationSerializer
from .services import user_service


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request: Request) -> Response:
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        data = user_service.login_user(request)

        return Response(data, status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = user_service.get_user_data(request)

        return Response(data, status=status.HTTP_200_OK)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = user_service.update_user_data(request)

        return Response(data, status=status.HTTP_200_OK)