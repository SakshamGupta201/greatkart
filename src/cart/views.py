from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from Product.models import Product
from cart.models import Cart, CartItem


def cart_view(request):
    cart_items = CartItem.objects.filter(cart__cart_id=_get_cart_id(request))
    context = {
        "cart_items": cart_items,
    }
    return render(request, "cart.html", context)


def _get_cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    _cart_id = _get_cart_id(request)
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id)

    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("cart_view")
