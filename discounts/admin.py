from django.contrib import admin

from discounts.models import (
    AutoShopPersonalDiscount,
    CarDiscount,
    GeneralDiscount,
    UserPersonalDiscount,
)

admin.site.register(GeneralDiscount)
admin.site.register(CarDiscount)
admin.site.register(UserPersonalDiscount)
admin.site.register(AutoShopPersonalDiscount)
