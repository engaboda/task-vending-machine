from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from account.models import User
from store.models import Product
from utils.random_values import random_str


class ProductViewsetTestCases(APITestCase):
    def setUp(self):
        self.seller = self.create_seller()
        self.product = Product.objects.create(
            seller=self.seller, amountAvailable=100, cost=100, productName="chai"
        )
        self.product_create_list_url = reverse('product-list')
        self.product_detail_update_destroy_url = reverse('product-detail', args=(self.product.id, ))

    def create_seller(self):
        user = User.create_objects.create_seller(username=random_str(), password=random_str())
        return user

    def test_product_detail(self):
        """
            getting of product details.
        """
        self.client.force_login(self.seller)
        response = self.client.get(self.product_detail_update_destroy_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(Product.objects.filter(seller=self.seller).exists(), True)

    def test_product_list(self):
        """
            list all product in db.
        """
        self.client.force_login(self.seller)
        response = self.client.get(self.product_create_list_url)
        self.assertTrue(isinstance(response.data, list))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.filter(seller=self.seller).exists(), True)

    def test_product_delete(self):
        """
            delete product.
        """
        self.client.force_login(self.seller)
        response = self.client.delete(self.product_detail_update_destroy_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.filter(id=self.product.id).exists(), False)

    def test_product_update_success(self):
        """
            update product.
        """
        self.client.force_login(self.seller)
        data = {
            'amountAvailable': 200,
        }
        response = self.client.patch(self.product_detail_update_destroy_url, data)
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.product.amountAvailable, data.get('amountAvailable'))

    def test_product_update_failed(self):
        """
            cant update because seller not the owner of product.
        """
        seller = self.create_seller()
        self.client.force_login(seller)
        data = {
            'amountAvailable': 1025,
        }
        response = self.client.patch(self.product_detail_update_destroy_url, data)
        self.assertEqual(response.status_code, 403)

    def test_product_create(self):
        """
            create product.
        """
        seller = self.create_seller()
        self.client.force_login(seller)
        data = {
            'amountAvailable': 100,
            'cost': '100.00',
            'productName': 'tom and jery',
        }
        response = self.client.post(self.product_create_list_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('amountAvailable'), data.get('amountAvailable'))
        self.assertEqual(response.data.get('cost'), data.get('cost'))
        self.assertEqual(response.data.get('productName'), data.get('productName'))
        self.assertTrue(Product.objects.filter(**data).exists())
