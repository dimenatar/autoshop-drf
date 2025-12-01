from typing import Dict, Any

from autoshops.models import AutoShop
from sales.models import SupplierSale, AutoShopSale


class AutoShopsService:
    @staticmethod
    def generate_statistics(shop_id) -> Dict[str, Any]:
        supplier_to_autoshop_sales = SupplierSale.objects.filter(autoshop_id_id=shop_id)
        autoshop_to_users_sales = AutoShopSale.objects.filter(autoshop_id_id=shop_id)
        autoshop = AutoShop.objects.filter(id=shop_id).first()

        income = round(sum([sale.price for sale in autoshop_to_users_sales]), 2)
        spend = round(sum([sale.price for sale in supplier_to_autoshop_sales]), 2)

        return {
            'sold cars count': autoshop_to_users_sales.count(),
            'income': income,
            'spend': spend,
            'profit': income - spend,
            'buyers': autoshop.buyers if autoshop else '-',
        }

    @staticmethod
    def generate_total_statistics() -> Dict[AutoShop, Dict[str, Any]]:
        return { shop: AutoShopsService.generate_statistics(shop.id) for shop in AutoShop.objects.all() }
