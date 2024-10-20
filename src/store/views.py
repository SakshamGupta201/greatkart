from django.shortcuts import render

from Product.models import Product
from category.models import Category


def store_view(request):

    products = Product.objects.all()
    context = {
        "products": products,
        "count": products.count(),
    }
    return render(request, "store.html", context)


def category_view(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=category)
    except Category.DoesNotExist:
        category = None
        products = Product.objects.none()

    context = {
        "products": products,
        "count": products.count(),
    }
    return render(request, "store.html", context)
