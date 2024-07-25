from django.contrib import admin
from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "order_date")

class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "price")

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity")

admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order_Product, OrderProductAdmin)