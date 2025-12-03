from django.contrib import admin

from offers.models import AutoShopOffer, UserOffer

admin.site.register(UserOffer)
admin.site.register(AutoShopOffer)
