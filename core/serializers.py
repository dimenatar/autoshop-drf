from typing import Any, Dict

from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    def get_current_user(self) -> Any:
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return request.user
        return None

    def is_admin_user(self) -> bool:
        user = self.get_current_user()
        return user and (user.is_superuser or user.is_staff)

    def validate_balance(self, value: float) -> float:
        if self.instance:
            original_balance = self.instance.balance
            if value != original_balance and not self.is_admin_user():
                raise serializers.ValidationError(
                    "You cannot change balance u pussy"
                )
        return value

    def update(self, instance: Any, validated_data: Dict[str, Any]) -> Any:
        if 'balance' in validated_data:
            self.validate_balance(float(validated_data['balance']))
        return validated_data
