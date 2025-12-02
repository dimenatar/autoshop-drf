from core.serializers import BaseModelSerializer
from suppliers.models import Supplier


class SupplierSerializer(BaseModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
