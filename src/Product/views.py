from django.views.generic import ListView
from Product.models import Product


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
            print(self.kwargs)
            context["product"] = Product.objects.get(pk=self.kwargs["pk"])
        except Product.DoesNotExist:
            context["product"] = None
        return context
