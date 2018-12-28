from django.contrib import admin
from precious_gifts.apps.store.models import Product, Order

admin.site.register(Product)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = (
        'order_summary',
    )
