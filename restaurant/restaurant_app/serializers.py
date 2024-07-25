from rest_framework import serializers
from .models import *
from datetime import datetime

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["order_id", "order_date"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if "T" in representation["order_date"]:
            date = datetime.strptime(representation["order_date"], "%Y-%m-%dT%H:%M:%SZ")
            representation["order_date"] = date.strftime("%Y-%m-%d %H:%M:%S")
        return representation

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["product_name", "price"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["price"] = float(representation["price"])
        return representation

class OrderProductSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    product = ProductSerializer()

    class Meta:
        model = Order_Product
        fields = ["order", "product", "quantity"]