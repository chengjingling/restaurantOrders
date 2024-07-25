import sys
import os
import django
from collections import defaultdict
import csv
from datetime import datetime
from django.utils import timezone
import pytz

sys.path.append("/Users/jingling/Desktop/SIM/Y3S1/CM3035 Advanced web development/Midterms/MIDTERM_PROJECT/restaurant")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant.settings")
django.setup()

from restaurant_app.models import *

order_data_file = "/Users/jingling/Desktop/SIM/Y3S1/CM3035 Advanced web development/Midterms/MIDTERM_PROJECT/restaurant-1-orders-edited.csv"
product_data_file = "/Users/jingling/Desktop/SIM/Y3S1/CM3035 Advanced web development/Midterms/MIDTERM_PROJECT/restaurant-1-products-price.csv"

orders = defaultdict(list)
products = defaultdict(list)
order_product = defaultdict(dict)

with open(order_data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    header = csv_reader.__next__()
    for row in csv_reader:
        unformatted_date = datetime.strptime(row[1], "%d/%m/%y %H:%M")
        formatted_date = unformatted_date.strftime("%Y-%m-%d %H:%M:%S")
        formatted_date_object = datetime.strptime(formatted_date, "%Y-%m-%d %H:%M:%S")
        formatted_date_gmt = timezone.make_aware(formatted_date_object, pytz.timezone("GMT"))
        orders[row[0]] = formatted_date_gmt
        order_product[row[0]][row[2]] = row[3]

with open(product_data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    header = csv_reader.__next__()
    for row in csv_reader:
        products[row[0]] = row[1]

Order.objects.all().delete()
Product.objects.all().delete()
Order_Product.objects.all().delete()

order_rows = {}
product_rows = {}

for order_id, order_date in orders.items():
    row = Order.objects.create(order_id=order_id,
                               order_date=order_date)
    row.save()
    order_rows[order_id] = row

for product_name, price in products.items():
    row = Product.objects.create(product_name=product_name,
                                 price=price)
    row.save()
    product_rows[product_name] = row

for order_id, data_dict in order_product.items():
    for key in data_dict.keys():
        row = Order_Product.objects.create(order=order_rows[order_id],
                                           product=product_rows[key],
                                           quantity=data_dict[key])
        row.save()