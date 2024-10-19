from django.shortcuts import render

from Product.models import Product
from category.models import Category


def store(request):
    products = Product.objects.all().filter(is_available=True).order_by("created_at")
    categories = Category.objects.all()
    context = {
        "products": products,
        "categories": categories,
        "count": products.count(),
    }
    return render(request, "store.html", context)
