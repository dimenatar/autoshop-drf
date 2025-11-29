from django.db import models
from core.models import BaseModel


class Sale(BaseModel):
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE)
    price = models.FloatField()
    discount_percent = models.FloatField()
    date = models.DateTimeField()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"date: {self.date}, car_id: {self.car}, price: {self.price}"


class AutoShopSale(Sale):
    autoshop = models.ForeignKey('autoshops.AutoShop', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{super().__str__()}, autoshop: {self.autoshop}, user_id {self.user}"


class SupplierSale(Sale):
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE)
    autoshop = models.ForeignKey('autoshops.AutoShop', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{super().__str__()}, autoshop: {self.autoshop}, supplier_id {self.supplier}"
