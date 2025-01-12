from django.contrib import admin

from discounts.models import GeneralDiscount, UserPersonalDiscount, CarDiscount

# Register your models here.
admin.site.register(GeneralDiscount)
admin.site.register(CarDiscount)
admin.site.register(UserPersonalDiscount)