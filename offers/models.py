from django.core.validators import MinValueValidator
from django.db import models
from cars.models import CarDetails
from core.models import BaseModel


class UserOffer(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE)
    max_price = models.FloatField(validators=[MinValueValidator(0.0)])

    def __str__(self) -> str:
        return (f'user: {self.user}, '
                f'car: {self.car}, max_price: {self.max_price}')


class AutoShopOffer(CarDetails):
    autoshop = models.ForeignKey('autoshops.AutoShop', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{super().__str__()}, autoshop: {self.autoshop}'
