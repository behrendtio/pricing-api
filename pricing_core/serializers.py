# pricing_core/serializers.py
from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('id', 'price', 'vat')


class ItemQuantitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="item.id")
    vat = serializers.ReadOnlyField(source="item.vat")
    price = serializers.ReadOnlyField(source="item.price")
    #something = serializers.SerializerMethodField()

    class Meta:
        model = models.ItemQuantity
        fields = ('id', 'quantity', 'price', 'vat')

    # The method for something
    def get_something(self, object):
        return object.item.price * object.quantity


class OrderSerializer(serializers.ModelSerializer):
    items = ItemQuantitySerializer(source="itemquantity_set", many=True, read_only=True)

    currency = serializers.ReadOnlyField(allow_null=True)

    class Meta:
        fields = ('id', 'customer', 'items', 'order_total', 'vat_total', 'currency')
        model = models.Order
