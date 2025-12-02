from core.serializers import BaseModelSerializer
from discounts.models import (
    AutoShopPersonalDiscount,
    CarDiscount,
    GeneralDiscount,
    UserPersonalDiscount,
)


class GeneralDiscountSerializer(BaseModelSerializer):
    class Meta:
        model = GeneralDiscount
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class UserPersonalDiscountSerializer(BaseModelSerializer):
    class Meta:
        model = UserPersonalDiscount
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class AutoShopPersonalDiscountSerializer(BaseModelSerializer):
    class Meta:
        model = AutoShopPersonalDiscount
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CarDiscountSerializer(BaseModelSerializer):
    class Meta:
        model = CarDiscount
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
