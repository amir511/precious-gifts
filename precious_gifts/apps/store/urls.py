from django.conf.urls import url
from precious_gifts.apps.store import views

app_name = 'store'

urlpatterns = [
    url(r'^products/$', views.ProductList.as_view(), name='product_list'),
    url(r'^product/(?P<pk>\d+)/$', views.ProductDetail.as_view(), name='product_detail'),
    url(r'^cart/view/$', views.view_cart, name='view_cart'), 
    url(r'^cart/add/(?P<product_pk>\d+)/(?P<quantity>\d+)/$', views.add_to_cart, name='add_to_cart'), 
    url(r'^cart/remove/(?P<product_pk>\d+)/$', views.remove_from_cart, name='remove_from_cart'), 

]