from django.core.validators import MinValueValidator
from django.db import models


class Car(models.Model):
    mark = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    horsepower = models.IntegerField(validators=[MinValueValidator(0)])
    year = models.IntegerField(validators=[MinValueValidator(0)], default=1800)

    def __str__(self):
         return f"brand: {self.brand}, mark: {self.mark}, horsepower: {self.horsepower}, year: {self.year}"

    class Meta:
        verbose_name = "Cars"
        verbose_name_plural = "Cars"
