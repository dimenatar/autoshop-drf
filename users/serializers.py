from core.serializers import BaseModelSerializer
from users.models import User


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
