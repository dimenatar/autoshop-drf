from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from cars.models import Car
from core.models import BaseModel


class BaseDiscount(BaseModel):
    percent = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f'{super().__str__()}, percent: {self.percent}%'

    class Meta:
        abstract = True

class GeneralDiscount(BaseDiscount):
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"{super().__str__()} name: {self.name} {super()} dates:{self.start_date}/{self.end_date}, description: {self.description}"

class BasePersonalDiscount(BaseDiscount):
    purchases_amount = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{super().__str__()}, purchases_amount: {self.purchases_amount}"

    class Meta:
        abstract = True

class UserPersonalDiscount(BasePersonalDiscount):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    autoshop = models.ForeignKey('autoshops.AutoShop', on_delete=models.CASCADE, default=0, null=True)

    def __str__(self):
        return f"user:{self.user} {super().__str__()}, autoshop: {self.autoshop}"

class AutoShopPersonalDiscount(BasePersonalDiscount):
    autoshop = models.ForeignKey('autoshops.AutoShop', on_delete=models.CASCADE, default=0, null=True)
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE)

    def __str__(self):
        return f"{super().__str__()} autoshop:{self.autoshop} supplier:{self.supplier}"

class CarDiscount(BaseDiscount):
    car = models.ManyToManyField(Car)

    def __str__(self):
        return f"car:{self.car} {super().__str__()}"