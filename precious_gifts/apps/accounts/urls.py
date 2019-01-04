from django.conf.urls import url
from precious_gifts.apps.accounts import views

app_name = 'accounts'

urlpatterns = [
    url(r'^sign-up/$', views.sign_up, name='sign_up'),
]