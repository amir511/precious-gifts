from django.shortcuts import render
from django.views.generic import ListView, DetailView
from precious_gifts.apps.store.models import Product

class ProductList(ListView):
    model = Product
    context_object_name = 'products'

class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'

