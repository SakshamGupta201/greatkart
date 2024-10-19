from django.urls import path
from cart import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_view, name="cart"),
    path("add/<slug:product_slug>/", views.add_to_cart, name="add_to_cart"),
]
