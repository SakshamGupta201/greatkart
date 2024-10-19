from django.db import models
from Product.models import Product


class Cart(models.Model):
    cart_id = models.CharField(max_length=50, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name
