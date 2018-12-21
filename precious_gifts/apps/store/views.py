from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from precious_gifts.apps.store.models import Product, Cart

class ProductList(ListView):
    model = Product
    context_object_name = 'products'

class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'

@login_required
def view_cart(request):
    try:
        cart = request.user.cart
    except ObjectDoesNotExist:
        cart = Cart(user=request.user)
        cart.save()

    return render(request, 'store/view_cart.html', {'cart':cart})
    
@login_required
def add_to_cart(request, product_pk, quantity):
    try:
        cart = request.user.cart
    except ObjectDoesNotExist:
        cart = Cart(user=request.user)
    
    product = Product.objects.get(pk=product_pk)
    try:
        cart.add_item(product, int(quantity))
        cart.save()
    except Exception as e:
        messages.error(request, e)

    return redirect('store:view_cart')

@login_required
def remove_from_cart(request, product_pk):
    
    cart = request.user.cart
    product = Product.objects.get(pk=product_pk)
    cart.remove_item(product)
    cart.save()

    return redirect('store:view_cart')

