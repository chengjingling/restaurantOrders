from rest_framework import generics, mixins, status
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CreateOrder(mixins.CreateModelMixin,
                  generics.GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        try:
            order_id = request.data.get("order_id")
            order_date = request.data.get("order_date")
            product_names = request.data.getlist("product_name")
            quantities = request.data.getlist("quantity")
    
            order_instance = Order.objects.create(
                order_id=order_id,
                order_date=order_date
            )

            product_data = []

            for i in range(len(product_names)):
                product_instance = Product.objects.get(product_name=product_names[i])
                order_product_instance = Order_Product.objects.create(
                    order=order_instance,
                    product=product_instance,
                    quantity=quantities[i]
                )
                product_data.append({
                    "product_name": product_names[i],
                    "price": product_instance.price,
                    "quantity": quantities[i]
                })

            data = {}
            data["order_id"] = order_id
            data["order_date"] = order_date
            data["product_data"] = product_data

            return Response(data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        order_products = Order_Product.objects.filter(order=instance)

        product_data = []
        for order_product in order_products:
            product_data.append({
                "product_name": order_product.product.product_name,
                "price": order_product.product.price,
                "quantity": order_product.quantity
            })

        data = serializer.data
        data["product_data"] = product_data

        return Response(data)

    def put(self, request, *args, **kwargs):
        try:
            order_id = request.data.get("hidden_order_id")
            order_date = request.data.get("order_date")
            product_names = request.data.getlist("product_name")
            quantities = request.data.getlist("quantity")
            
            order_instance = self.get_object()
            order_instance.order_date = order_date
            order_instance.save()

            order_products = Order_Product.objects.filter(order=order_instance)
            order_products.delete()

            product_data = []

            for i in range(len(product_names)):
                product_instance = Product.objects.get(product_name=product_names[i])
                order_product_instance = Order_Product.objects.create(
                    order=order_instance,
                    product=product_instance,
                    quantity=int(quantities[i])
                )
                product_data.append({
                    "product_name": product_names[i],
                    "price": product_instance.price,
                    "quantity": int(quantities[i])
                })

            data = {}
            data["order_id"] = int(order_id)
            data["order_date"] = order_date
            data["product_data"] = product_data

            return Response(data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CreateProduct(mixins.CreateModelMixin,
                  generics.GenericAPIView):
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        try:
            product_name = request.data.get("product_name")
            price = request.data.get("price")

            product_instance = Product.objects.create(
                product_name=product_name,
                price=price
            )

            data = {}
            data["product_name"] = product_name
            data["price"] = price

            return Response(data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)