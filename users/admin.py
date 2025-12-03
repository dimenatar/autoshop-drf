from typing import Any

from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role', 'balance', 'age')
    list_filter = ('role',)
    search_fields = ('name', 'email')

    fields = ('name', 'email', 'age', 'telephone', 'role', 'balance', 'password')

    readonly_fields = ('balance',)

    def get_fields(self, request: Any, obj: Any = None) -> Any:
        if obj is None:
            return 'name', 'email', 'age', 'telephone', 'role', 'password'
        return super().get_fields(request, obj)

    def save_model(self, request: Any, obj: Any, form: Any, change: bool) -> None:
        if not change:
            obj.balance = 0
        super().save_model(request, obj, form, change)
