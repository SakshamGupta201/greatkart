from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "stock",
        "category",
        "updated_at",
        "is_available",
    )
    search_fields = ("name", "category__name")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Product, ProductAdmin)
