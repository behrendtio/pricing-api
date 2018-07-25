# pricing_core/serializers.py
from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('id', 'price', 'vat')


class ItemQuantitySerializer(serializers.ModelSerializer):
    order = serializers.ReadOnlyField(source='*')
    product = serializers.ReadOnlyField(source='*')  # passing all
    #order = OrderSerializer(read_only=True)
    #product = ProductSerializer(read_only=True)

    class Meta:
        model = models.ItemQuantity
        fields = ('quantity')


class OrderSerializer(serializers.ModelSerializer):
    items = ProductSerializer(many=True, read_only=True)
    quantity = ItemQuantitySerializer(source='*', read_only=True)

    #currency = (allow_null = True)

    class Meta:
        fields = ('id', 'customer', 'items', 'quantity', 'order_total', 'vat_total')
        model = models.Order
