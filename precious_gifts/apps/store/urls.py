from django.conf.urls import url
from precious_gifts.apps.store.views import ProductList, ProductDetail


urlpatterns = [
    url(r'^products/$', ProductList.as_view(), name='product_list'),
    url(r'^product/(?P<pk>\d+)/$', ProductDetail.as_view(), name='product_detail'),
]