from django.db import models

from autoshops.models import AutoShop
from cars.models import Car
from suppliers.models import Supplier
from users.models import User

class Sale(models.Model):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_price = models.FloatField()
    price = models.FloatField()
    discount_percent = models.FloatField()
    discount_amount = models.FloatField()
    date = models.DateField()

    class Meta:
        abstract = True

    def __str__(self):
        return f"date: {self.date}, car_id: {self.car_id} start_price: {self.start_price}, actual_price: {self.price}, discount_percent: {self.discount_percent}, discount_amount: {self.discount_amount}"

class AutoShopSale(Sale):
    autoshop_id = models.ForeignKey(AutoShop, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{super()}, autoshop: {self.autoshop_id}, user_id {self.user_id}"

class SupplierSale(Sale):
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    autoshop_id = models.ForeignKey(AutoShop, on_delete=models.CASCADE)

    def __str__(self):
        return f"{super()}, autoshop: {self.autoshop_id}, supplier_id {self.supplier_id}"