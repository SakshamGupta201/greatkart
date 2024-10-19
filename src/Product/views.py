from django.shortcuts import render
from django.views.generic import ListView
from Product.models import Product


class ProductList(ListView):
    template_name = "index.html"
    queryset = Product.objects.all().filter(is_available=True)
    context_object_name = "products"
