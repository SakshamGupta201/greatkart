from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from Product.models import Product
from category.models import Category


def paginate_products(request, products_list):
    products_list = products_list.order_by("slug")
    paginator = Paginator(products_list, 10)
    page = request.GET.get("page")
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return products


def store_view(request):
    products_list = Product.objects.all()
    products = paginate_products(request, products_list)

    context = {
        "products": products,
        "count": products_list.count(),
    }
    return render(request, "store.html", context)


def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products_list = Product.objects.filter(category=category)
    products = paginate_products(request, products_list)

    context = {
        "products": products,
        "count": products_list.count(),
    }
    return render(request, "store.html", context)


def product_search_view(request):
    if "q" in request.GET:
        keyword = request.GET["q"]
        if keyword:
            products_list = Product.objects.filter(
                Q(name__icontains=keyword) | Q(description__icontains=keyword)
            ).order_by("-created_at")
        else:
            products_list = Product.objects.all()
    products = paginate_products(request, products_list)

    context = {
        "products": products,
        "count": products_list.count(),
    }
    return render(request, "store.html", context)
