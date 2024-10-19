from django.contrib import admin
from cart.models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    # list_display = ["cart_id", "date_added"]
    readonly_fields = ["cart_id", "date_added"]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ["product", "cart", "quantity", "active"]
    list_filter = ["active"]
    search_fields = ["product", "cart"]
    readonly_fields = ["cart"]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
