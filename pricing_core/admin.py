from django.contrib import admin

from pricing_core.models import Product, Order, ItemQuantity


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ItemQuantity)
