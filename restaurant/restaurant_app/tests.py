from rest_framework.test import APITestCase
from .model_factories import *
from .serializers import *
from django.urls import reverse
import json
from django.db.utils import IntegrityError

class OrderSerializerTest(APITestCase):
    order1 = None
    orderserializer = None

    def setUp(self):
        self.order1 = OrderFactory.create(order_id=1, order_date="2023-12-26 13:46:00")
        self.orderserializer = OrderSerializer(instance=self.order1)

    def tearDown(self):
        Order.objects.all().delete()
        Product.objects.all().delete()
        Order_Product.objects.all().delete()
        OrderFactory.reset_sequence(0)
        ProductFactory.reset_sequence(0)
        OrderProductFactory.reset_sequence(0)

    def test_orderSerializerHasCorrectFields(self):
        data = self.orderserializer.data
        self.assertEqual(set(data.keys()), set(["order_id", "order_date"]))

    def test_orderSerializerHasCorrectData(self):
        data = self.orderserializer.data
        self.assertEqual(data["order_id"], 1)
        self.assertEqual(data["order_date"], "2023-12-26 13:46:00")

class ProductSerializerTest(APITestCase):
    product1 = None
    productserializer = None

    def setUp(self):
        self.product1 = ProductFactory.create(product_name="Garlic Naan", price=2.95)
        self.productserializer = ProductSerializer(instance=self.product1)

    def tearDown(self):
        Order.objects.all().delete()
        Product.objects.all().delete()
        Order_Product.objects.all().delete()
        OrderFactory.reset_sequence(0)
        ProductFactory.reset_sequence(0)
        OrderProductFactory.reset_sequence(0)

    def test_productSerializerHasCorrectFields(self):
        data = self.productserializer.data
        self.assertEqual(set(data.keys()), set(["product_name", "price"]))

    def test_productSerializerHasCorrectData(self):
        data = self.productserializer.data
        self.assertEqual(data["product_name"], "Garlic Naan")
        self.assertEqual(data["price"], 2.95)

class OrderProductSerializerTest(APITestCase):
    order1 = None
    product1 = None
    orderproduct1 = None
    orderproductserializer = None

    def setUp(self):
        self.order1 = OrderFactory.create(order_id=1, order_date="2023-12-26 13:46:00")
        self.product1 = ProductFactory.create(product_name="Garlic Naan", price=2.95)
        self.orderproduct1 = OrderProductFactory.create(order=self.order1, product=self.product1, quantity=1)
        self.orderproductserializer = OrderProductSerializer(instance=self.orderproduct1)

    def tearDown(self):
        Order.objects.all().delete()
        Product.objects.all().delete()
        Order_Product.objects.all().delete()
        OrderFactory.reset_sequence(0)
        ProductFactory.reset_sequence(0)
        OrderProductFactory.reset_sequence(0)

    def test_orderproductSerializerHasCorrectFields(self):
        data = self.orderproductserializer.data
        self.assertEqual(set(data.keys()), set(["order", "product", "quantity"]))

    def test_orderproductSerializerHasCorrectData(self):
        data = self.orderproductserializer.data
        self.assertEqual(data["order"]["order_id"], 1)
        self.assertEqual(data["order"]["order_date"], "2023-12-26 13:46:00")
        self.assertEqual(data["product"]["product_name"], "Garlic Naan")
        self.assertEqual(data["product"]["price"], 2.95)
        self.assertEqual(data["quantity"], 1)

class OrderListTest(APITestCase):
    order1 = None
    order2 = None
    good_url = ""
    bad_url = ""

    def setUp(self):
        self.order1 = OrderFactory.create(order_id=1, order_date="2023-12-26 13:46:00")
        self.order2 = OrderFactory.create(order_id=2, order_date="2023-12-26 14:23:00")
        self.good_url = reverse("order_list_api")
        self.bad_url = "/api/bad_url"

    def tearDown(self):
        Order.objects.all().delete()
        Product.objects.all().delete()
        Order_Product.objects.all().delete()
        OrderFactory.reset_sequence(0)
        ProductFactory.reset_sequence(0)
        OrderProductFactory.reset_sequence(0)

    def test_orderListReturnsSuccess(self):
        response = self.client.get(self.good_url, format="json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn({"order_id": 1, "order_date": "2023-12-26 13:46:00"}, data)
        self.assertIn({"order_id": 2, "order_date": "2023-12-26 14:23:00"}, data)

    def test_orderListReturnsFailureOnBadUrl(self):
        response = self.client.get(self.bad_url, format="json")
        self.assertEqual(response.status_code, 404)

class CreateOrderTest(APITestCase):
    order1 = None
    product1 = None
    product2 = None
    good_url = ""
    bad_url = ""
    good_data = {}
    bad_data = {}
    data_with_existing_id = {}

    def setUp(self):
        self.order1 = OrderFactory.create(order_id=1, order_date="2023-12-26 13:46:00")
        self.product1 = ProductFactory.create(product_name="Plain Naan", price=2.6)
        self.product2 = ProductFactory.create(product_name="Garlic Naan", price=2.95)
        self.good_url = reverse("create_order_api")
        self.bad_url = "/api/bad_url"
        self.good_data = {
            "order_id": 2,
            "order_date": "2023-12-26 14:23:00",
            "product_name": ["Plain Naan", "Garlic Naan"],
            "quantity": [1, 2]
        }
        self.bad_data = {
            "field1": 1,
            "field2": 2
        }
        self.data_with_existing_id = {
            "order_id": 1,
            "order_date": "2023-12-26 14:23:00",
            "product_name": ["Plain Naan", "Garlic Naan"],
            "quantity": [1, 2]
        }

    def tearDown(self):
        try:
            with transaction.atomic():
                Order.objects.all().delete()
                Product.objects.all().delete()
                Order_Product.objects.all().delete()
                OrderFactory.reset_sequence(0)
                ProductFactory.reset_sequence(0)
                OrderProductFactory.reset_sequence(0)
        except Exception as e:
            print(f"Error during CreateOrderTest tearDown: {e}")

    def test_createOrderReturnsSuccess(self):
        response = self.client.post(self.good_url, self.good_data, format="multipart")
        self.assertEqual(response.status_code, 201)

    def test_createOrderReturnsFailureOnBadUrl(self):
        response = self.client.post(self.bad_url, self.good_data, format="multipart")
        self.assertEqual(response.status_code, 404)

    def test_createOrderReturnsFailureOnBadData(self):
        response = self.client.post(self.good_url, self.bad_data, format="multipart")
        self.assertEqual(response.status_code, 400)

    def test_createOrderReturnsFailureOnExistingOrderId(self):
        response = self.client.post(self.good_url, self.data_with_existing_id, format="multipart")
        self.assertEqual(response.status_code, 400)

class OrderDetailTest(APITestCase):
    order1 = None
    product1 = None
    product2 = None
    orderproduct1 = None
    good_url = ""
    bad_url = ""
    original_data = {}
    input_data = {}
    updated_data = {}
    bad_data = {}

    def setUp(self):
        self.order1 = OrderFactory.create(order_id=1, order_date="2023-12-26 13:46:00")
        self.product1 = ProductFactory.create(product_name="Plain Naan", price=2.6)
        self.product2 = ProductFactory.create(product_name="Garlic Naan", price=2.95)
        self.orderproduct1 = OrderProductFactory.create(order=self.order1, product=self.product1, quantity=1)
        self.good_url = reverse("order_detail_api", kwargs={"pk": 1})
        self.bad_url = "/api/bad_url"
        self.original_data = {
            "order_id": 1,
            "order_date": "2023-12-26 13:46:00",
            "product_data": [
                {"product_name": "Plain Naan", "price": 2.6, "quantity": 1}
            ]
        }
        self.input_data = {
            "hidden_order_id": 1,
            "order_date": "2023-12-26 14:23:00",
            "product_name": ["Plain Naan", "Garlic Naan"],
            "quantity": [1, 2]
        }
        self.updated_data = {
            "order_id": 1,
            "order_date": "2023-12-26 14:23:00",
            "product_data": [
                {"product_name": "Plain Naan", "price": 2.6, "quantity": 1},
                {"product_name": "Garlic Naan", "price": 2.95, "quantity": 2}
            ]
        }
        self.bad_data = {
            "field1": 1,
            "field2": 2
        }

    def tearDown(self):
        try:
            with transaction.atomic():
                Order.objects.all().delete()
                Product.objects.all().delete()
                Order_Product.objects.all().delete()
                OrderFactory.reset_sequence(0)
                ProductFactory.reset_sequence(0)
                OrderProductFactory.reset_sequence(0)
        except Exception as e:
            print(f"Error during OrderDetailTest tearDown: {e}")

    def test_orderDetailReturnsSuccess(self):
        response = self.client.get(self.good_url, format="json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data, self.original_data)

    def test_orderDetailReturnsFailureOnBadUrl(self):
        response = self.client.get(self.bad_url, format="json")
        self.assertEqual(response.status_code, 404)

    def test_updateOrderReturnsSuccess(self):
        response = self.client.put(self.good_url, self.input_data, format="multipart")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data, self.updated_data)

    def test_updateOrderReturnsFailureOnBadData(self):
        with self.assertRaises(IntegrityError):
            response = self.client.put(self.good_url, self.bad_data, format="multipart")

    def test_deleteOrderReturnsSuccess(self):
        response = self.client.delete(self.good_url, format="json")
        self.assertEqual(response.status_code, 204)

class ProductListTest(APITestCase):
    product1 = None
    product2 = None
    good_url = ""
    bad_url = ""

    def setUp(self):
        self.product1 = ProductFactory.create(product_name="Plain Naan", price=2.6)
        self.product2 = ProductFactory.create(product_name="Garlic Naan", price=2.95)
        self.good_url = reverse("product_list_api")
        self.bad_url = "/api/bad_url"

    def tearDown(self):
        Order.objects.all().delete()
        Product.objects.all().delete()
        Order_Product.objects.all().delete()
        OrderFactory.reset_sequence(0)
        ProductFactory.reset_sequence(0)
        OrderProductFactory.reset_sequence(0)

    def test_productListReturnsSuccess(self):
        response = self.client.get(self.good_url, format="json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn({"product_name": "Plain Naan", "price": 2.6}, data)
        self.assertIn({"product_name": "Garlic Naan", "price": 2.95}, data)

    def test_productListReturnsFailureOnBadUrl(self):
        response = self.client.get(self.bad_url, format="json")
        self.assertEqual(response.status_code, 404)

class CreateProductTest(APITestCase):
    product1 = None
    good_url = ""
    bad_url = ""
    good_data = {}
    bad_data = {}
    data_with_existing_name = {}

    def setUp(self):
        self.product1 = ProductFactory.create(product_name="Plain Naan", price=2.6)
        self.good_url = reverse("create_product_api")
        self.bad_url = "/api/bad_url"
        self.good_data = {
            "product_name": "Garlic Naan",
            "price": 2.95
        }
        self.bad_data = {
            "field1": 1,
            "field2": 2
        }
        self.data_with_existing_name = {
            "product_name": "Plain Naan",
            "price": 2.95
        }

    def tearDown(self):
        try:
            with transaction.atomic():
                Order.objects.all().delete()
                Product.objects.all().delete()
                Order_Product.objects.all().delete()
                OrderFactory.reset_sequence(0)
                ProductFactory.reset_sequence(0)
                OrderProductFactory.reset_sequence(0)
        except Exception as e:
            print(f"Error during CreateProductTest tearDown: {e}")

    def test_createProductReturnsSuccess(self):
        response = self.client.post(self.good_url, self.good_data, format="multipart")
        self.assertEqual(response.status_code, 201)

    def test_createProductReturnsFailureOnBadUrl(self):
        response = self.client.post(self.bad_url, self.good_data, format="multipart")
        self.assertEqual(response.status_code, 404)

    def test_createProductReturnsFailureOnBadData(self):
        response = self.client.post(self.good_url, self.bad_data, format="multipart")
        self.assertEqual(response.status_code, 400)

    def test_createProductReturnsFailureOnExistingProductName(self):
        response = self.client.post(self.good_url, self.data_with_existing_name, format="multipart")
        self.assertEqual(response.status_code, 400)