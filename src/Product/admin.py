from django.contrib import admin
from Product.models import Product, Variation


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


class VariationAdmin(admin.ModelAdmin):
    list_display = ("product", "category", "value", "active")
    list_editable = ("active",)
    list_filter = ("product", "category", "value", "active")


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
