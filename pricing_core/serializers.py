# pricing_core/serializers.py
from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('id', 'price', 'vat')


class OrderSerializer(serializers.ModelSerializer):
    items = ProductSerializer(many=True, read_only=True)

    class Meta:
        fields = ('id', 'customer', 'items', 'order_total', 'vat_total')
        model = models.Order
