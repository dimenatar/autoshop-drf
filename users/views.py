from rest_framework.request import Request
from rest_framework.response import Response

from core.views import ViewBase
from users.services import UserService


class UserStatisticsView(ViewBase):
    def get(self, request: Request) -> Response:
        return self.generate_final_response_to_single_entity(request, UserService.generate_statistics)


class UsersTotalStatisticsView(ViewBase):
    def get(self, request: Request) -> Response:
        return Response(UserService.generate_total_statistics())
