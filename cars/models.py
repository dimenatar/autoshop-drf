from django.db import models


class Cars(models.Model):
    mark = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    horsepower = models.FloatField(blank=True, null=True)
