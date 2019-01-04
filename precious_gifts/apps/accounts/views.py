from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from precious_gifts.apps.accounts.models import Buyer
from precious_gifts.apps.accounts.forms import NewBuyerForm, NewUserForm, LoginForm


def sign_up(request):
    if request.method == 'POST':
        user_form = NewUserForm(request.POST)
        buyer_form = NewBuyerForm(request.POST)
        if user_form.is_valid() and buyer_form.is_valid():
            try:
                user = user_form.save()
                buyer = buyer_form.save(commit=False)
                buyer.user = user
                buyer.save()
                messages.success(request, 'Welcome to Precious Gifts, enjoy!')
                return redirect('store:product_list')
            except Exception as e:
                messages.success(request, 'The following error has occured: {}'.format(str(e)))
        else:
            [messages.error(request, error[0]) for error in user_form.errors.values()]
            [messages.error(request, error[0]) for error in buyer_form.errors.values()]
    else:
        user_form = NewUserForm()
        buyer_form = NewBuyerForm()
    context = {'user_form': user_form, 'buyer_form': buyer_form}
    return render(request, 'accounts/sign_up.html', context=context)


def log_in(request):
    pass

