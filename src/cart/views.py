from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from Product.models import Product
from cart.models import Cart, CartItem


def cart_view(request):
    cart_items = CartItem.objects.filter(cart__cart_id=_get_cart_id(request))
    total_price = float(
        sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    )
    tax = round(0.1 * total_price, 2)
    grand_total = round(total_price + tax, 2)

    context = {
        "cart_items": cart_items,
        "total_price": round(total_price, 2),
        "tax": tax,
        "grand_total": grand_total,
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

    return redirect("cart:cart")


def update_cart_item_quantity(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get("quantity"))
        cart_item.quantity = quantity
        cart_item.save()
        sub_total = cart_item.sub_total()
        total = float(
            sum(
                cart_item.product.price * cart_item.quantity
                for cart_item in CartItem.objects.filter(
                    cart__cart_id=_get_cart_id(request)
                )
            )
        )
        return JsonResponse(
            {
                "success": True,
                "sub_total": sub_total,
                "total": total,
            }
        )

    else:
        return JsonResponse(
            {"success": False, "error": "Invalid request method"}, status=400
        )


def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    sub_total = cart_item.sub_total()
    total = float(
        sum(
            cart_item.product.price * cart_item.quantity
            for cart_item in CartItem.objects.filter(
                cart__cart_id=_get_cart_id(request)
            )
        )
    )
    return JsonResponse(
        {
            "success": True,
            "sub_total": sub_total,
            "total": total,
        }
    )
