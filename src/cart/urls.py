from django.urls import path
from cart import views

urlpatterns = [
    path("", views.cart_view, name="cart"),
]
