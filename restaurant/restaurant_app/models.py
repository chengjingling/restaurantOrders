from django.db import models

class Order(models.Model):
    order_id = models.IntegerField(primary_key=True, null=False, blank=False)
    order_date = models.DateTimeField(null=False, blank=False)

    class Meta:
        ordering = ['-order_id']

class Product(models.Model):
    product_name = models.CharField(max_length=100, primary_key=True, null=False, blank=False)
    price = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)

class Order_Product(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)

    class Meta:
        unique_together = ["order", "product"]