from cars.models import Car
from core.serializers import BaseModelSerializer


class CarSerializer(BaseModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
