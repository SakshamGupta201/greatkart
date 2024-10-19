from django.shortcuts import render

from Product.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    products_list = Product.objects.all().filter(is_available=True)
    paginator = Paginator(products_list, 10)  # Show 10 products per page

    page = request.GET.get("page")
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        "products": products,
    }
    return render(request, "index.html", context)
