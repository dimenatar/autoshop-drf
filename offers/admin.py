from django.contrib import admin

from offers.models import UserToAutoShopOffer, AutoShopToSupplierOffer

# Register your models here.
admin.site.register(UserToAutoShopOffer)
admin.site.register(AutoShopToSupplierOffer)
