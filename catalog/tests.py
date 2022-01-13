from django.test import TestCase
from catalog.models import Products, Offers
from rest_framework.test import APIClient
from api.v1.products.views import offer_updater
from django.core import serializers
import json


# Create your tests here.


class DatabaseTestCase(TestCase):
    """
    Database creation test case
    """

    @classmethod
    def setUpClass(cls):
        super(DatabaseTestCase, cls).setUpClass()
        cls.product = Products(id=1, name="Lemrarna", description="test1")
        cls.product.save()
        cls.offer1 = Offers(offer_id=000000, price=1000, items_in_stock=0, product=cls.product)
        cls.offer1.save()
        cls.offer2 = Offers(offer_id=111111, price=0, items_in_stock=100, product=cls.product)
        cls.offer2.save()

    def test_creation(self):
        self.assertEqual(self.product.name, 'Lemrarna')
        self.assertEqual(self.product.description, 'test1')
        self.assertEqual(True, self.product == self.offer1.product)
        self.assertEqual(True, self.product == self.offer2.product)


class APITestCase(TestCase):

    def test_CRUD(self):
        client = APIClient()

        r1 = client.post('/api/v1/products/create', {'name': "Humpquarna", 'description': "test2"})
        self.assertEquals(r1.status_code, 201)
        self.assertEquals(r1.data['status'], True)
        self.assertEquals(r1.data['data']["name"], "Humpquarna")
        self.assertEquals(r1.data['data']["description"], "test2")

        product_id = str(r1.data["data"]["id"])

        r2 = client.put('/api/v1/products/' + product_id, {'name': "Lessquarna", 'description': "test3"})
        self.assertEquals(r2.status_code, 200)
        self.assertTrue(r2.data['status'])

        r3 = client.get('/api/v1/products/' + product_id)
        self.assertEquals(r3.status_code, 200)
        self.assertEquals(str(r3.data['id']), product_id)
        self.assertEquals(r3.data['name'], "Lessquarna")
        self.assertEquals(r3.data['description'], "test3")

        r5 = client.get('/api/v1/products/' + product_id + "/offers")
        self.assertEquals(r5.status_code, 200)
        self.assertTrue('Offers' in r5.data)

        self.assertEquals(offer_updater(), 1)

        r4 = client.delete('/api/v1/products/' + product_id)
        self.assertEquals(r4.status_code, 204)
        self.assertTrue(r4.data['status'])

        self.assertEquals(offer_updater(), 0)
