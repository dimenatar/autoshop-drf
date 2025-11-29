from abc import abstractmethod
from typing import Any

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from cars.models import Car
from core.models import BaseModel


class BaseDiscount(BaseModel):
    percent = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self) -> str:
        return f'percent: {self.percent}%'

    class Meta:
        abstract = True


class GeneralDiscount(BaseDiscount):
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.TextField()
    description = models.TextField()

    def __str__(self) -> str:
        return f"{super().__str__()}, name: {self.name}"


class BasePersonalDiscount(BaseDiscount):
    purchases_amount = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return f"{super().__str__()}, purchases_amount: {self.purchases_amount}"

    @abstractmethod
    def is_suitable_discount(self, shop: Any, buyer: Any) -> bool:
        return False

    class Meta:
        abstract = True


class UserPersonalDiscount(BasePersonalDiscount):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    autoshop = models.ForeignKey('autoshops.AutoShop', on_delete=models.CASCADE,
                                 default=0, null=True)

    def __str__(self) -> str:
        return f"user:{self.user} {super().__str__()}, autoshop: {self.autoshop}"

    def is_suitable_discount(self, shop: Any, buyer: Any) -> bool:
        return self.objects.filter(user=buyer, autoshop=shop).exists()

    def get_full_discount_percent(self) -> float:
        return self.percent


class AutoShopPersonalDiscount(BasePersonalDiscount):
    autoshop = models.ForeignKey('autoshops.AutoShop', on_delete=models.CASCADE,
                                 default=0, null=True)
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE)
    required_cars_bought_amount = models.IntegerField(validators=[MinValueValidator(0)])
    increasing_percent_per_requirements_fulfilled = (
        models.FloatField
        (
            validators=[MinValueValidator(0), MaxValueValidator(100)]
        ))

    def __str__(self) -> str:
        return f"{super().__str__()} autoshop:{self.autoshop} supplier:{self.supplier}"

    def get_full_discount_percent(self) -> float:
        return (self.purchases_amount // self.required_cars_bought_amount) + self.percent

    def is_suitable_discount(self, shop: Any, buyer: Any) -> bool:
        return self.objects.filter(autoshop=buyer, supplier=shop).exists()


class CarDiscount(BaseDiscount):
    cars = models.ManyToManyField(Car)

    def __str__(self) -> str:
        return f"car:{self.cars} {super().__str__()}"
