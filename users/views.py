from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from .renderers import UserJSONRenderer
from .services import user_service
from .serializers import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request: Request) -> Response:
        try:
            data = user_service.register_user(request)
            return Response(data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response(
                {'errors': e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'errors': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def get(self, request: Request) -> Response:
        return redirect('/login')

    def post(self, request: Request) -> Response:
        try:
            data = user_service.login_user(request)
            return Response(data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(
                {'errors': e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)

    def retrieve(self, request: Request, *args: dict, **kwargs: dict) -> Response:
        data = user_service.get_user_data(request)
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request: Request, *args: dict, **kwargs: dict) -> Response:
        try:
            data = user_service.update_user_data(request)
            return Response(data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(
                {'errors': e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )


class EmailVerificationAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request, token: str) -> Response:
        success = user_service.verify_email(request, token)
        if success:
            return Response(
                {'message': 'Email verified successfully'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'Invalid or expired verification token'},
            status=status.HTTP_400_BAD_REQUEST
        )


class PasswordResetRequestAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        success = user_service.request_password_reset(email)

        if success:
            return Response(
                {'message': 'Password reset instructions have been sent to your email'},
                status=status.HTTP_200_OK
            )


class PasswordResetConfirmAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request, token: str) -> Response:
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data['new_password']
        success = user_service.reset_password(token, new_password)

        if success:
            return Response(
                {'message': 'Password has been reset successfully'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'Invalid or expired reset token'},
            status=status.HTTP_400_BAD_REQUEST
        )


class EmailVerifiedView(TemplateView):
    template_name = 'account/email_verified.html'
