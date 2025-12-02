from core.views import BaseListView, BaseSingleItemView
from discounts.models import (
    AutoShopPersonalDiscount,
    CarDiscount,
    GeneralDiscount,
    UserPersonalDiscount,
)
from discounts.serializers import (
    AutoShopPersonalDiscountSerializer,
    CarDiscountSerializer,
    GeneralDiscountSerializer,
    UserPersonalDiscountSerializer,
)


class GeneralDiscountListView(BaseListView):
    queryset = GeneralDiscount.objects.all()
    serializer_class = GeneralDiscountSerializer


class GeneralDiscountView(BaseSingleItemView):
    queryset = GeneralDiscount.objects.all()
    serializer_class = GeneralDiscountSerializer


class UserPersonalDiscountListView(BaseListView):
    queryset = UserPersonalDiscount.objects.all()
    serializer_class = UserPersonalDiscountSerializer


class UserPersonalDiscountView(BaseSingleItemView):
    queryset = UserPersonalDiscount.objects.all()
    serializer_class = UserPersonalDiscountSerializer


class AutoShopPersonalDiscountListView(BaseListView):
    queryset = AutoShopPersonalDiscount.objects.all()
    serializer_class = AutoShopPersonalDiscountSerializer


class AutoShopPersonalDiscountView(BaseSingleItemView):
    queryset = AutoShopPersonalDiscount.objects.all()
    serializer_class = AutoShopPersonalDiscountSerializer


class CarDiscountListView(BaseListView):
    queryset = CarDiscount.objects.all()
    serializer_class = CarDiscountSerializer


class CarDiscountView(BaseSingleItemView):
    queryset = CarDiscount.objects.all()
    serializer_class = CarDiscountSerializer
