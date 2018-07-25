from django.contrib import admin

from pricing_core.models import Product, Order


admin.site.register(Product)
admin.site.register(Order)
