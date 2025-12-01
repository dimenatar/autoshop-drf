from typing import Any, Dict

from suppliers.models import Supplier


class SupplierService:
    @staticmethod
    def generate_statistics(supplier_id: int) -> Dict[str, Any]:
        sales = Supplier.objects.filter(id=supplier_id)

        return {
            'sold_cars_amount': sales.count(),
            'profit': round(sum([sale.price for sale in sales]), 2)
        }

    @staticmethod
    def generate_total_statistics() -> Dict[str, Dict[str, Any]]:
        return {supplier: SupplierService.generate_statistics(supplier.id) for supplier in Supplier.objects.all()}
