from django.conf.urls import url
from precious_gifts.apps.accounts import views

app_name = 'accounts'

urlpatterns = [
    url(r'^signup/$', views.sign_up, name='sign_up'),
    url(r'^login/$', views.log_in, name='log_in'),
    url(r'^logout/$', views.log_out, name='log_out'),
]