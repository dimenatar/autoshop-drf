from core.views import BaseListView, BaseSingleItemView
from suppliers.models import Supplier
from suppliers.serializers import SupplierSerializer


class SupplierListView(BaseListView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplierView(BaseSingleItemView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
