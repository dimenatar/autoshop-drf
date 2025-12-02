from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.request import Request
from rest_framework.response import Response


class BaseSingleItemView(GenericAPIView,  RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.retrieve(request,  *args, **kwargs)

    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.destroy(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.partial_update(request, *args, **kwargs)


class BaseListView(GenericAPIView, ListModelMixin, CreateModelMixin):
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.create(request, *args, **kwargs)

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.list(request, *args, **kwargs)
