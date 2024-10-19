from category.models import Category


def menu_links(request):
    categories = Category.objects.all().order_by("name")
    return dict(categories=categories)


def price_options(request):
    price_options = [50, 100, 150, 200, 500, 1000, 2000]
    return dict(price_options=price_options)
