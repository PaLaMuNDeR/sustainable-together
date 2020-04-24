from __future__ import absolute_import
from django.test import TestCase
from django.test import RequestFactory, TestCase
# from .views import ClientViewSet
from django.test import Client
from rest_framework.test import APIClient

# Create your tests here.

class Register(TestCase):
    """
        Test Registration and Login
    """

    def setUp(self):

        # Every test needs access to the request factory.
        self.client = APIClient()

    def register(self):
        """
        Test Register
        :return:
        """
        new_client = {'username': 'martin', 'password':'test', 'email': 'martianev@gmail.com', 'firstname': 'martin', 'lastname': 'anev'}

        # Create an instance of a POST request.
        response = self.client.post('/api/user/register/', data=new_client)
        # Test the view
        self.assertEqual(response.status_code, 200)

    def register_test_user(self):
        """
        Test Register
        :return:
        """
        new_client = {'username': 'test', 'password':'test', 'email': 'martianev@gmail.com', 'firstname': 'martin', 'lastname': 'anev'}

        # Create an instance of a POST request.
        response = self.client.post('/api/user/register/', data=new_client)
        # Test the view
        self.assertEqual(response.status_code, 200)

    def register_with_existing_user(self):
        """
        Test Register
        :return:
        """
        new_client = {'username': 'martin', 'password':'test', 'email': 'martianev@gmail.com', 'firstname': 'martin', 'lastname': 'anev'}

        # Create an instance of a POST request.
        response = self.client.post('/api/user/register/', data=new_client)
        # Test the view
        self.assertEqual(response.status_code, 403)

    def login(self, username, password):
        """
        Test of a correct login
        :param username:
        :param password:
        :return:
        """
        client = {'username': username, 'password': password}
        response=self.client.post('/api/user/login/', data=client)
        self.assertEqual(response.status_code, 200)
        return response.data['token']

    def bad_login(self, username, password):
        """
        Test bad login
        :param username:
        :param password:
        :return:
        """
        client = {'username': username, 'password': password}
        response=self.client.post('/api/user/login/', data=client)
        self.assertEqual(response.status_code, 400)

    def get_profile(self, token):
        """
        Get a profile
        :param token:
        :return:
        """
        client = {'username': 'martin', 'email': 'newmail@gmail.com', 'firstname': 'martin', 'lastname': 'anev'}
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token)
        response = self.client.get('/api/user/get_profile/', data=client)
        self.assertEqual(response.status_code, 200)

    def edit_profile(self, token):
        """
        Edit a profile
        :param token:
        :return:
        """
        client = {'username': 'martin', 'email': 'newmail@gmail.com', 'firstname': 'martin', 'lastname': 'anev'}
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token)
        response = self.client.put('/api/user/1/', data=client)
        self.assertEqual(response.status_code, 200)

    def edit_profile_of_another_user(self, token):
        """
        Edit a profile of another user should fail
        :param token:
        :return:
        """
        client = {'username': 'martin', 'email': 'newmail@gmail.com', 'firstname': 'martin', 'lastname': 'anev'}
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token)
        response = self.client.put('/api/user/1/', data=client)
        self.assertEqual(response.status_code, 400)

    def test_01_register_and_login(self):
        self.register()
        self.register_with_existing_user()
        token = self.login('martin','test')
        self.bad_login('martin','wrong password')
        self.get_profile(token)
        self.edit_profile(token)
        self.add_meal(token)
        self.edit_meal(token)
        self.get_meal(token)
        self.register_test_user()
        token2 = self.login('test','test')
        self.add_meal(token2)
        self.edit_meal_of_another_user(token2)
        self.edit_profile_of_another_user(token2)


