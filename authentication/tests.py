import json

from authentication.models import User

from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserRegistrationAPIViewTestCase(APITestCase):
    url = reverse("users:list")

    def test_invalid_password(self):
        """
        Test to verify that a post call with invalid passwords
        """
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "password",
            "confirm_password": "INVALID_PASSWORD"
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_user_registration(self):
        """
        Test to verify that a post call with user valid data
        """
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "123123",
            "confirm_password": "123123"
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)
        self.assertTrue("token" in json.loads(response.content))

    def test_unique_username_validation(self):
        """
        Test to verify that a post call with already exists username
        """
        user_data_1 = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "123123",
            "confirm_password": "123123"
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(201, response.status_code)

        user_data_2 = {
            "username": "testuser",
            "email": "test2@testuser.com",
            "password": "123123",
            "confirm_password": "123123"
        }
        response = self.client.post(self.url, user_data_2)
        self.assertEqual(400, response.status_code)


class UserLoginAPIViewTestCase(APITestCase):
    url = reverse("users:login")

    def setUp(self):
        self.username = "ameen"
        self.email = "ameen@gmail.com"
        self.password = "actual_password"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"username": "someuser"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(self.url, {"username": self.username, "password": "not_actual_password"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("auth_token" in json.loads(response.content))

    def test_authentication_with_not_activated_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.url, {"username": self.username, "password": self.password})
        self.assertEqual(400, response.status_code)


class UserPasswordChangeTestCase(APITestCase):
    url = reverse("users:password_change")

    def setUp(self):
        self.username = "ameen"
        self.email = "ameen@gmail.com"
        self.password = "actual_password"
        self.user = User.objects.create_user(
            self.username,
            self.email,
            self.password
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_invalid_original_password(self):
        data = {
            "old_password": "some-wrong-password",
            "new_password": "somePassword12%#"
        }
        response = self.client.put(self.url, data=data)
        self.assertTrue("non_field_errors" in json.loads(response.content))
        self.assertTrue("Old password is invalid" in json.loads(response.content)["non_field_errors"])
        self.assertEqual(400, response.status_code)

    def test_with_valid_data(self):
        new_password = "strongPassword12%#"
        data = {
            "old_password": self.password,
            "new_password": new_password
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(200, response.status_code)

        self.user = User.objects.get(username=self.username)
        self.assertTrue(self.user.check_password(new_password))

    def test_without_old_password_field(self):
        data = {
            "old_password": self.password,
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(400, response.status_code)

    def test_without_new_password_field(self):
        data = {
            "new_password": "strongPassword12%#",
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(400, response.status_code)

    def test_change_password_without_login_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ')
        new_password = "somePassword12%#"
        data = {
            "old_password": self.password,
            "new_password": new_password
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(401, response.status_code)

    def test_new_weak_password(self):
        new_password = "123456"
        data = {
            "old_password": self.password,
            "new_password": new_password
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(400, response.status_code)


class UserTokenAPIViewTestCase(APITestCase):
    def url(self, key):
        return reverse("users:token", kwargs={"key": key})

    def setUp(self):
        self.username = "ameen"
        self.email = "ameen@gmail.com"
        self.password = "actual_password"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        self.user_2 = User.objects.create_user("ahmed", "ahmed@earth.com", "super_secret")
        self.token_2 = Token.objects.create(user=self.user_2)

    def tearDown(self):
        self.user.delete()
        self.token.delete()
        self.user_2.delete()
        self.token_2.delete()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_delete_by_key(self):
        response = self.client.delete(self.url(self.token.key))
        self.assertEqual(204, response.status_code)
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

    def test_delete_current(self):
        response = self.client.delete(self.url('current'))
        self.assertEqual(204, response.status_code)
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

    def test_delete_unauthorized(self):
        response = self.client.delete(self.url(self.token_2.key))
        self.assertEqual(404, response.status_code)
        self.assertTrue(Token.objects.filter(key=self.token_2.key).exists())

    def test_get(self):
        # Test that unauthorized access returns 404
        response = self.client.get(self.url(self.token_2.key))
        self.assertEqual(404, response.status_code)

        for key in [self.token.key, 'current']:
            response = self.client.get(self.url(key))
            self.assertEqual(200, response.status_code)
            self.assertEqual(self.token.key, response.data['auth_token'])
            self.assertIn('created', response.data)