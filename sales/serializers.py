from core.serializers import BaseModelSerializer
from sales.models import AutoShopSale, SupplierSale


class AutoShopSaleSerializer(BaseModelSerializer):
    class Meta:
        model = AutoShopSale
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class SupplierSaleSerializer(BaseModelSerializer):
    class Meta:
        model = SupplierSale
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
