from django.urls import path
from Product import views

urlpatterns = [
    path("", views.ProductList.as_view(), name="products"),
]
