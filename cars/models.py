from django.core.validators import MinValueValidator
from django.db import models
from core.models import BaseModel


class CarDetails(BaseModel):
    max_price = models.FloatField(validators=[MinValueValidator(0.0)], null=True, blank=True)
    desired_brand = models.CharField(null=True, max_length=50)
    desired_model = models.CharField(null=True, max_length=50)
    min_horsepower = models.IntegerField(validators=[MinValueValidator(0)], null=True)
    max_horsepower = models.IntegerField(validators=[MinValueValidator(0)], null=True)
    min_year = models.IntegerField(validators=[MinValueValidator(0)], null=True)
    max_year = models.IntegerField(validators=[MinValueValidator(0)], null=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return (f'{super().__str__()},'
                f' desired brand: {self.desired_brand}, desired model: {self.desired_model}')


class Car(BaseModel):
    model = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    horsepower = models.IntegerField(validators=[MinValueValidator(0)])
    year = models.IntegerField(validators=[MinValueValidator(0)], default=1800)

    def __str__(self) -> str:
        return (f"{super().__str__()}, brand: {self.brand}, model: {self.model}, "
                f"year: {self.year}")

    class Meta:
        verbose_name = "Cars"
        verbose_name_plural = "Cars"
