from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)]) #sorry drandma
    telephone = models.CharField(max_length=13)
    balance = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"name: {self.name}, age: {self.age}, telephone: {self.telephone}"