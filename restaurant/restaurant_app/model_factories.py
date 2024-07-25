import factory
from .models import *

class OrderFactory(factory.django.DjangoModelFactory):
    order_id = 1
    order_date = "2023-12-16 13:27:00"

    class Meta:
        model = Order

class ProductFactory(factory.django.DjangoModelFactory):
    product_name = "Plain Naan"
    price = 1.95

    class Meta:
        model = Product

class OrderProductFactory(factory.django.DjangoModelFactory):
    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 1

    class Meta:
        model = Order_Product