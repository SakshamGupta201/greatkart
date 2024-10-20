from cart.models import CartItem
from cart.views import _get_cart_id


def counter(request):
    cart_items = CartItem.objects.filter(cart__cart_id=_get_cart_id(request))
    return {
        "cart_count": cart_items.count(),
    }
