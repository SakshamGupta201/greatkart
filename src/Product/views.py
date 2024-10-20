from django.views.generic import ListView
from Product.models import Product
from cart.models import CartItem
from cart.views import _get_cart_id


class ProductList(ListView):
    template_name = "index.html"
    queryset = Product.objects.all().filter(is_available=True)
    context_object_name = "products"


class ProductDetail(ListView):
    template_name = "product_detail.html"
    queryset = Product.objects.all().filter(is_available=True)
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            in_cart = CartItem.objects.filter(
                cart__cart_id=_get_cart_id(self.request),
                product__pk=self.kwargs["pk"],
            ).exists()
            context["in_cart"] = in_cart
            context["product"] = Product.objects.get(pk=self.kwargs["pk"])
        except Product.DoesNotExist:
            context["product"] = None
        return context
