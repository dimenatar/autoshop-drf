from rest_framework.request import Request
from rest_framework.response import Response

from core.views import ViewBase
from suppliers.services import SupplierService


class SupplierStatisticsView(ViewBase):
    def __init__(self):
        super().__init__()
        self.entity_name = 'supplier'

    def get(self, request: Request) -> Response:
        return self.generate_final_response_to_single_entity(request, SupplierService.generate_statistics)


class SuppliersTotalStatisticsView(ViewBase):
    def __init__(self):
        super().__init__()
        self.entity_name = 'autoshop'

    def get(self, request: Request) -> Response:
        return Response(SupplierService.generate_total_statistics())
