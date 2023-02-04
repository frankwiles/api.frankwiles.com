from django.contrib import admin

from .models import CounterType, Counter


@admin.register(CounterType)
class CounterTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "active")
    list_filter = ("active",)


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ("type", "count", "created")
    list_filter = ("type",)
    list_select_related = ("type",)
    date_hierarchy = "created"
