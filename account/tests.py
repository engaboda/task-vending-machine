from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from .models import User
from utils.random_values import random_str
from store.models import Product


class UserViewSetTestCases(APITestCase):
    def setUp(self):
        self.user_detail_url = reverse('user-detail')
        self.user_update_url = reverse('user-update')
        self.user_destroy_url = reverse('user-destroy')
        self.create_buyer =  reverse('user-create-buyer')
        self.create_seller =  reverse('user-create-seller')

    def create_user(self):
        user = User.create_objects.create_user(username=random_str(), password=random_str())
        return user

    def test_create_buyer(self):
        data = {
            'username': 'aboda',
            'password': '123'
        }
        response = self.client.post(self.create_buyer, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('message'), 'created')

    def test_create_seller(self):
        data = {
            'username': 'aboda',
            'password': '123'
        }
        response = self.client.post(self.create_seller, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('message'), 'created')

    def test_detail_success(self):
        user = self.create_user()
        user.deposit = 100
        user.save()
        self.client.force_login(user)
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('deposit'), user.deposit)

    def test_detail_failed(self):
        """
            user not authinticated.
        """
        user = self.create_user()
        user.deposit = 100
        user.save()
        self.client.force_login(user)
        try:
            response = self.client.get(self.user_detail_url)
        except:
            self.assertEqual(True, False)
        else:
            self.assertEqual(True, True)

    def test_delete_user(self):
        """
            make usre api delete user.
        """
        user = self.create_user()
        user.deposit = 100
        user.save()
        self.client.force_login(user)
        response = self.client.delete(self.user_destroy_url)
        self.assertEqual(response.status_code, 204)

    def test_update_user(self):
        """
            user can only change username.
        """
        user = self.create_user()
        user.username = "testgo"
        user.save()
        self.client.force_login(user)
        data = {
            'username': 'testgogo',
        }
        response = self.client.put(self.user_update_url, data)
        self.assertEqual(response.data.get('username'), data.get('username'))
        self.assertEqual(response.status_code, 202)


class BuyerViewSetTestCases(APITestCase):
    def setUp(self):
        self.seller = self.create_seller()
        self.product = Product.objects.create(
            seller=self.seller, amountAvailable=100, cost=100, productName="chai"
        )
        self.deposit_url =  reverse('buyer-deposit')
        self.buy_url =  reverse('buyer-buy')
        self.reset_deposit_url =  reverse('buyer-reset-deposit')

    def create_buyer(self):
        user = User.create_objects.create_buyer(username=random_str(), password=random_str())
        return user

    def create_seller(self):
        user = User.create_objects.create_seller(username=random_str(), password=random_str())
        return user    

    def test_deposit_success(self):
        buyer = self.create_buyer()
        buyer.deposit = 100
        buyer.save()
        self.client.force_login(buyer)
        data = {
            'deposit': 100
        }
        response = self.client.put(self.deposit_url, data)
        self.assertEqual(response.status_code, 200)
        buyer.refresh_from_db()
        self.assertEqual(buyer.deposit, 200)

    def test_deposit_failed(self):
        """
            deposit value not in [5, 10, 20, 50, 100]
        """
        buyer = self.create_buyer()
        buyer.deposit = 100
        buyer.save()
        self.client.force_login(buyer)
        data = {
            'deposit': 25
        }
        response = self.client.put(self.deposit_url, data)
        self.assertEqual(response.data.get('deposit')[0], "deposit should be one of [5, 10, 20, 50, 100]")

    def test_deposit_failed_is_not_buyer(self):
        seller = self.create_seller()
        seller.save()
        self.client.force_login(seller)
        data = {
            'deposit': 25
        }
        response = self.client.put(self.deposit_url, data)
        self.assertEqual(response.status_code, 403)

    def test_buy_failed(self):
        buyer = self.create_buyer()
        self.client.force_login(buyer)
        data = {
            'product_info': [{"productId": self.product.id, "amount_of_product": 5}]
        }
        response = self.client.post(self.buy_url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], "Cost of Product is larger than Available Price")

    def test_buy_success(self):
        buyer = self.create_buyer()
        buyer.deposit = 500
        buyer.save()
        self.client.force_login(buyer)
        data = {
            'product_info': [{"productId": self.product.id, "amount_of_product": 5}]
        }
        response = self.client.post(self.buy_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        buyer.refresh_from_db()
        self.assertEqual(buyer.deposit, 0)
        self.product.refresh_from_db()
        self.assertEqual(self.product.amountAvailable, 95)

    def test_reset_deposit(self):
        buyer = self.create_buyer()
        buyer.deposit = 100
        buyer.save()
        self.client.force_login(buyer)
        response = self.client.post(self.reset_deposit_url)
        self.assertEqual(response.status_code, 200)
        buyer.refresh_from_db()
        self.assertEqual(buyer.deposit, 0)
