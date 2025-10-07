from django.db import models
from core.models import BaseModel


class Sale(BaseModel):
    car_id = models.ForeignKey('cars.Car', on_delete=models.CASCADE)
    price = models.FloatField()
    discount_percent = models.FloatField()
    date = models.DateField()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return (f"date: {self.date}, car_id: {self.car_id},"
                f" price: {self.price}")


class AutoShopSale(Sale):
    autoshop_id = models.ForeignKey('autoshops.AutoShop', on_delete=models.CASCADE)
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{super().__str__()}, autoshop: {self.autoshop_id}, user_id {self.user_id}"


class SupplierSale(Sale):
    supplier_id = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE)
    autoshop_id = models.ForeignKey('autoshops.AutoShop', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return (f"{super().__str__()}, autoshop: {self.autoshop_id},"
                f" supplier_id {self.supplier_id}")
