from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from precious_gifts.apps.accounts.models import Buyer
from precious_gifts.apps.accounts.forms import NewBuyerForm, NewUserForm, LoginForm
from precious_gifts.apps.mail.utils import send_fast_mail
from uuid import uuid4

def sign_up(request):
    # Clearing old messages first to avoid duplicate message display
    old_messages = messages.get_messages(request)
    old_messages.used = True
    if request.method == 'POST':
        user_form = NewUserForm(request.POST)
        buyer_form = NewBuyerForm(request.POST)
        if user_form.is_valid() and buyer_form.is_valid():
            try:
                user = user_form.save(commit=False)
                password = user_form.cleaned_data['password']
                user.set_password(password)
                user.is_active = False
                user.save()
                buyer = buyer_form.save(commit=False)
                buyer.user = user
                buyer.activation_key = str(uuid4())
                buyer.save()
                activation_link = request.get_host() + '/accounts/activate-user/' + buyer.activation_key + '/'
                activation_link = 'http://' + activation_link if not activation_link.startswith('http') else activation_link
                email_context = {
                    'user_name': user.username,
                    'activation_link': activation_link,
                }
                send_fast_mail(user.email, 'new_user_signup', email_context)
                messages.success(request, 'An email has been sent to you to complete the registration process.')
                return redirect('accounts:log_in')
            except Exception as e:
                messages.error(request, 'The following error has occured: {}'.format(str(e)))
        else:
            [messages.error(request, error[0]) for error in user_form.errors.values()]
            [messages.error(request, error[0]) for error in buyer_form.errors.values()]
    else:
        user_form = NewUserForm()
        buyer_form = NewBuyerForm()
    context = {'user_form': user_form, 'buyer_form': buyer_form}
    return render(request, 'accounts/sign_up.html', context=context)

def activate_user(request, key):
    try:
        buyer = Buyer.objects.get(activation_key=key)
        buyer.user.is_active = True
        buyer.user.save()
        messages.success(request, 'Your account is now active!, log in to continue.')
    except Buyer.DoesNotExist:
        messages.error(request, 'Invalid activation link!')
    
    return redirect('accounts:log_in')

def log_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Log in successful.')
                return redirect('store:product_list')
            else:
                messages.error(request, "Couldn't log in, please try again.")
    form = LoginForm()
    context = {'form': form}
    return render(request, 'accounts/log_in.html', context=context)


def log_out(request):
    logout(request)
    messages.success(request, 'Logged out succesfully')
    return redirect('store:product_list')

