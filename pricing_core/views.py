# from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from pricing_core.models import Order, ItemQuantity
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "get", "head", "options"]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        for item in self.request.data.get("items"):
            instance.items.add(item["id"])

    @action(methods=['get'], detail=False)
    def calculate_currency_price(self, request):
        order_id = request.data.get("id")
        user_currency = request.data.get("user_currency")
        order = Order.objects.get(id=order_id)

        serializer = OrderSerializer(order)
        if order:
            converted = order.get_converted_order_total(user_currency=user_currency)
            return Response({'converted_order_total': converted,
                             'order': serializer.data})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
