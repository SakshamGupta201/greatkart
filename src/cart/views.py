from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from Product.models import Product, Variation
from cart.models import Cart, CartItem
from django.db.models import Q


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


from django.db.models import Count, Q


def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    variation_products = []

    if request.method == "POST":
        variation_products = [
            Variation.objects.get(
                product=product, category__iexact=key, value__iexact=value
            )
            for key, value in request.POST.items()
            if Variation.objects.filter(
                product=product, category__iexact=key, value__iexact=value
            ).exists()
        ]

    cart_id = _get_cart_id(request)
    cart, _ = Cart.objects.get_or_create(cart_id=cart_id)

    cart_items = CartItem.objects.filter(product=product, cart=cart)

    if variation_products:
        variations_filter = Q()
        for variation in variation_products:
            variations_filter |= Q(variation=variation)

        cart_items = (
            cart_items.filter(variations_filter)
            .annotate(variation_count=Count("variation"))
            .filter(variation_count=len(variation_products))
        )

        matching_cart_items = [
            cart_item
            for cart_item in cart_items
            if set(cart_item.variation.all()) == set(variation_products)
        ]

        if matching_cart_items:
            cart_item = matching_cart_items[0]
            cart_item.quantity += 1
        else:
            cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
            cart_item.variation.set(variation_products)
    else:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)

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
