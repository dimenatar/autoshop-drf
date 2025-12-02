from autoshops.models import AutoShop
from autoshops.serializers import AutoShopSerializer
from core.views import BaseListView, BaseSingleItemView


class AutoShopListView(BaseListView):
    queryset = AutoShop.objects.all()
    serializer_class = AutoShopSerializer


class AutoShopView(BaseSingleItemView):
    queryset = AutoShop.objects.all()
    serializer_class = AutoShopSerializer
