from django.contrib import admin
from precious_gifts.apps.store.models import Product, Order

admin.site.register((Product, Order))

