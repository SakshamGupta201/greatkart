from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from Product.models import Product, Variation
from cart.models import Cart, CartItem


def cart_view(request):
    cart_items = CartItem.objects.filter(cart__cart_id=_get_cart_id(request))
    total_price, tax, grand_total = _calculate_totals(cart_items)

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


def _calculate_totals(cart_items):
    total_price = float(sum(item.product.price * item.quantity for item in cart_items))
    tax = round(0.1 * total_price, 2)
    grand_total = round(total_price + tax, 2)
    return total_price, tax, grand_total


def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    variation_products = []
    if request.method == "POST":
        for key, value in request.POST.items():
            print(f"{key}: {value}")
            try:
                variation = Variation.objects.get(
                    product=product, category__iexact=key, value=value
                )
                variation_products.append(variation)
            except Variation.DoesNotExist:
                continue

    cart_id = _get_cart_id(request)
    cart, _ = Cart.objects.get_or_create(cart_id=cart_id)

    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
    if variation_products:
        cart_item.variation.clear()
        cart_item.variation.set(variation_products)
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("cart:cart")


def update_cart_item_quantity(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.quantity = int(request.POST.get("quantity"))
        cart_item.save()

        cart_items = CartItem.objects.filter(cart__cart_id=_get_cart_id(request))
        total_price, tax, _ = _calculate_totals(cart_items)

        return JsonResponse(
            {
                "success": True,
                "sub_total": cart_item.sub_total(),
                "total": total_price,
                "tax": tax,
            }
        )
    else:
        return JsonResponse(
            {"success": False, "error": "Invalid request method"}, status=400
        )


def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()

    cart_items = CartItem.objects.filter(cart__cart_id=_get_cart_id(request))
    total_price, tax, _ = _calculate_totals(cart_items)

    return JsonResponse(
        {
            "success": True,
            "sub_total": cart_item.sub_total(),
            "total": total_price,
            "tax": tax,
        }
    )
