from django.conf.urls import url
from precious_gifts.apps.store import views

app_name = 'store'

urlpatterns = [
    url(r'^$', views.product_list, name='product_list'),
    url(r'^product/(?P<pk>\d+)/$', views.ProductDetail.as_view(), name='product_detail'),
    url(r'^cart/$', views.view_cart, name='view_cart'),
    url(r'^cart/add/(?P<product_pk>\d+)/(?P<quantity>\d+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^cart/remove/(?P<product_pk>\d+)/$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^cart/checkout/$', views.checkout, name='checkout'),
    url(r'^orders/$', views.order_list, name='order_list'),
    url(r'^order/(?P<pk>\d+)/$', views.order_detail, name='order_detail'),
    url(r'^order/cancel/(?P<pk>\d+)/$', views.cancel_order, name='cancel_order'),
]
