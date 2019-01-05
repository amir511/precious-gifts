from django.contrib import admin
from precious_gifts.apps.store.models import Product, Order, ShippingFees

admin.site.register((Product, ShippingFees,))

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = (
        'order_summary',
    )
