from django.urls import path
from . import views
from . import api

urlpatterns = [
    path("", views.index, name="index"),
    path("orders", views.order_list, name="order_list"),
    path("order/new", views.create_order, name="create_order"),
    path("order/<int:pk>", views.order_detail, name="order_detail"),
    path("order/<int:pk>/update", views.update_order, name="update_order"),
    path("products", views.product_list, name="product_list"),
    path("product/new", views.create_product, name="create_product"),

    path("api/orders", api.OrderList.as_view(), name="order_list_api"),
    path("api/order/new", api.CreateOrder.as_view(), name="create_order_api"),
    path("api/order/<int:pk>", api.OrderDetail.as_view(), name="order_detail_api"),
    path("api/products", api.ProductList.as_view(), name="product_list_api"),
    path("api/product/new", api.CreateProduct.as_view(), name="create_product_api"),
]