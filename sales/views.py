from core.views import BaseListView, BaseSingleItemView
from sales.models import AutoShopSale, SupplierSale
from sales.serializers import AutoShopSaleSerializer, SupplierSaleSerializer


class AutoShopSaleListView(BaseListView):
    queryset = AutoShopSale.objects.all()
    serializer_class = AutoShopSaleSerializer


class AutoShopSaleView(BaseSingleItemView):
    queryset = AutoShopSale.objects.all()
    serializer_class = AutoShopSaleSerializer


class SupplierSaleListView(BaseListView):
    queryset = SupplierSale.objects.all()
    serializer_class = SupplierSaleSerializer


class SupplierSaleView(BaseSingleItemView):
    queryset = SupplierSale.objects.all()
    serializer_class = SupplierSaleSerializer
