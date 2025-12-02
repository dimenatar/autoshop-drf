from autoshops.models import AutoShop
from core.serializers import BaseModelSerializer


class AutoShopSerializer(BaseModelSerializer):
    class Meta:
        model = AutoShop
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
