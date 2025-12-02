from core.serializers import BaseModelSerializer
from offers.models import AutoShopOffer, UserOffer


class UserOffersSerializer(BaseModelSerializer):
    class Meta:
        model = UserOffer
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class AutoShopOffersSerializer(BaseModelSerializer):
    class Meta:
        model = AutoShopOffer
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
