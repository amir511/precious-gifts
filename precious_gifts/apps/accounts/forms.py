from django import forms
from django.contrib.auth.models import User
from precious_gifts.apps.accounts.models import Buyer


class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {'password': forms.PasswordInput()}


class NewBuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        exclude = ('user',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.PasswordInput()
