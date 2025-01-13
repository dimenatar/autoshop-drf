from django.core.validators import MinValueValidator
from django.db import models

from cars.models import CarDetails

class UserToAutoShopOffer(CarDetails):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    autoshop = models.ForeignKey('autoshops.AutoShop', on_delete=models.CASCADE)

    def __str__(self):
        return f'{super().__str__()}, user: {self.user}, autoshop: {self.autoshop}'

class AutoShopToSupplierOffer(CarDetails):
    autoshop = models.ForeignKey('autoshops.AutoShop', on_delete=models.CASCADE)
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE)

    def __str__(self):
        return f'{super().__str__()}, autoshop: {self.autoshop}, supplier: {self.supplier}'