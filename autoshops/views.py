from rest_framework.request import Request
from rest_framework.response import Response

from autoshops.services import AutoShopsService
from core.views import ViewBase


class AutoShopStatisticsView(ViewBase):
    def __init__(self) -> None:
        super().__init__()
        self.entity_name = 'autoshop'

    def get(self, request: Request) -> Response:
        return self.generate_final_response_to_single_entity(request,  AutoShopsService.generate_statistics)


class AutoShopsTotalStatisticsView(ViewBase):
    def __init__(self) -> None:
        super().__init__()
        self.entity_name = 'autoshop'

    def get(self, request: Request) -> Response:
        return Response(AutoShopsService.generate_total_statistics())
