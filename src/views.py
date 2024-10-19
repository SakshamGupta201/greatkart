from django.shortcuts import render
from django.views.generic import TemplateView


class Store(TemplateView):
    template_name = "store/store.html"
