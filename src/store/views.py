from django.shortcuts import render

from Product.models import Product
from category.models import Category

categories = Category.objects.all().order_by("name")
price_options = [50, 100, 150, 200, 500, 1000, 2000]


def store_view(request):

    products = Product.objects.all().filter(is_available=True)
    context = {
        "price_options": price_options,
        "products": products,
        "categories": categories,
        "count": products.count(),
    }
    return render(request, "store.html", context)


def category_view(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    except Category.DoesNotExist:
        category = None
        products = Product.objects.none()

    context = {
        "price_options": price_options,
        "products": products,
        "categories": categories,
        "count": products.count(),
    }
    return render(request, "store.html", context)
