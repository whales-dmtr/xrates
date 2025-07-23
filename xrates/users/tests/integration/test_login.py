from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthTestCase(TestCase):
    USERNAME = 'user'
    PASSWORD = 'secure1234'


class LoginTest(AuthTestCase):
    def setUp(self):
        data = {
            'username': self.USERNAME,
            'password1': self.PASSWORD,
            'password2': self.PASSWORD,
        }
        self.client.post(reverse('users:register'), data=data)

    def login(self, username, password): 
        data = {
            'username': username,
            'password': password,
        }
        response = self.client.post(reverse('users:login'), data=data)
        return response

    def test_login(self):
        self.assertRedirects(
            self.login(self.USERNAME, self.PASSWORD), 
            reverse('rates')
        )

    def test_login_as_unknown_user(self):
        self.assertContains(
            self.login('another_user', '1234'),
            'Please enter a correct username and password. ' \
            'Note that both fields may be case-sensitive.'
        )

    def test_get_login_page(self):
        self.client.cookies.clear()
        self.assertContains(
            self.client.get(reverse('users:login')),
            text='input',
            count=3
        )

    def tearDown(self):
        User.objects.all().delete()