from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .models import User


class UserTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="TESTPASSWORD")

    def tearDown(self):
        self.user.delete()

    def test_get_users_no_token(self):
        response = self.client.get('/api/get_users')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_users_token(self):
        self.token, self.created = Token.objects.get_or_create(user=self.user)

        response = self.client.get(path='/api/get_users',  HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.assertEqual(response.data['users'][0]['username'], self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_bad_username(self):
        response = self.client.post(path='/api/login', data={"username": "wrongtest", "password": "TESTPASSWORD"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_bad_password(self):
        response = self.client.post(path='/api/login', data={"username": "testuser", "password": "wrongpassword"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_correct(self):
        response = self.client.post(path='/api/login', data={"username": "testuser","password": "TESTPASSWORD"})

        self.token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['user']['username'], self.user.username)
        self.assertEqual(response.data['token'], self.token.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
