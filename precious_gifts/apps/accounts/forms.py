from django import forms
from django.contrib.auth.models import User
from precious_gifts.apps.accounts.models import Buyer


class NewUserForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {'password': forms.PasswordInput()}
    
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('confirm_password') == cleaned_data.get('password'):
            raise forms.ValidationError("Passwords Doesn't match!")
        email_exists = User.objects.filter(email=cleaned_data.get('email'))
        if email_exists:
            raise forms.ValidationError('This email address already exists!')
            
class NewBuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        exclude = ('user',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput())
