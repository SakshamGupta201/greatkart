from django.urls import path
from Product import views

app_name = "product"

urlpatterns = [
    path("", views.ProductList.as_view(), name="products"),
    path("<slug:pk>/", views.ProductDetail.as_view(), name="product_detail"),
]
