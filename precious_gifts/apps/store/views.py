from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from precious_gifts.apps.store.models import Product, Cart, Order
from precious_gifts.apps.store.forms import ChangeQtyForm


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'


def product_list(request):
    product_list = Product.objects.all()
    product_paginator = Paginator(product_list, 12)
    page = request.GET.get('page')
    try:
        products = product_paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = product_paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = product_paginator.page(product_paginator.num_pages)

    return render(request, 'store/product_list.html', {'products': products})


@login_required
def view_cart(request):
    try:
        cart = request.user.cart
    except ObjectDoesNotExist:
        cart = Cart(user=request.user)
        cart.save()
    if request.method == 'POST':
        form = ChangeQtyForm(request.POST)
        if form.is_valid():
            new_quantity = form.cleaned_data['new_quantity']
            item_pk = form.cleaned_data['item_pk']
            item = cart.items.get(pk=item_pk)
            if item.product.remaining_stock < new_quantity:
                messages.error(request, "Quantity is bigger than the available stock!")
            else:
                item.quantity = new_quantity
                item.save()
                messages.success(request, "Quantity updated successfully!")
        else:
            messages.error(request, "Quantity couldn't be updated!")
    form = ChangeQtyForm()
    context = {'cart': cart, 'form': form}
    return render(request, 'store/view_cart.html', context=context)


@login_required
def add_to_cart(request, product_pk, quantity):
    try:
        cart = request.user.cart
    except ObjectDoesNotExist:
        cart = Cart(user=request.user)
        cart.save()

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


@login_required
def checkout(request):

    cart = request.user.cart
    try:
        order = cart.create_order()
    except Exception as e:
        messages.error(request, e)
        return redirect('store:view_cart')
    return redirect('store:order_detail', pk=order.pk)


@login_required
def order_list(request):

    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'store/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    if order.user != request.user:
        return HttpResponseForbidden("<h1>Access Denied! </h1>")
    return render(request, 'store/order_detail.html', {'order': order})


@login_required
def cancel_order(request, pk):
    order = Order.objects.get(pk=pk)  # type: Order
    if order.user != request.user or order.status != 'Under Preparation':
        return HttpResponseForbidden("<h1>Access Denied! </h1>")
    order.status = 'Cancelled'
    order.save()
    messages.success(request, 'Order has been cancelled!')
    return render(request, 'store/order_detail.html', {'order': order})

