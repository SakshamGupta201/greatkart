from django.urls import path
from store import views

app_name = "store"

urlpatterns = [
    path("", views.store_view, name="store"),
    path("<slug:category_slug>/", views.category_view, name="category_detail"),
]
