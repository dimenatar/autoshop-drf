from typing import Any, Dict

from sales.models import AutoShopSale
from users.models import User


class UserService:
    @staticmethod
    def generate_statistics(user_id: int) -> Dict[str, Any]:

        user_data = User.objects.filter(pk=user_id).first()
        autoshop_sales = AutoShopSale.objects.filter(user_id__id=user_id)

        return {
            'registration date': user_data.created_at if user_data else '-',
            'cars bought': autoshop_sales.count(),
            'money lost': round(sum([sale.price for sale in autoshop_sales]), 2)
        }

    @staticmethod
    def generate_total_statistics() -> Dict[str, Dict[str, Any]]:
        return {user: UserService.generate_statistics(user.id) for user in User.objects.all()}
