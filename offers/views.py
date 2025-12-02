from core.views import BaseListView, BaseSingleItemView
from offers.models import AutoShopOffer, UserOffer
from offers.serializers import AutoShopOffersSerializer, UserOffersSerializer


class UserOfferListView(BaseListView):
    queryset = UserOffer.objects.all()
    serializer_class = UserOffersSerializer


class UserOfferView(BaseSingleItemView):
    queryset = UserOffer.objects.all()
    serializer_class = UserOffersSerializer


class AutoShopOfferListView(BaseListView):
    queryset = AutoShopOffer.objects.all()
    serializer_class = AutoShopOffersSerializer


class AutoShopOfferView(BaseSingleItemView):
    queryset = AutoShopOffer.objects.all()
    serializer_class = AutoShopOffersSerializer
