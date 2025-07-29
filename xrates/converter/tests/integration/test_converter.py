from django.urls import reverse

from users.tests.integration.test_login import AuthTestCase
from converter.models import ConverterHistory


class ConverterTest(AuthTestCase):
    def setUp(self):
        register_data = {
            'username': self.USERNAME,
            'password1': self.PASSWORD,
            'password2': self.PASSWORD,
        }
        login_data = {
            'username': self.USERNAME,
            'password': self.PASSWORD,
        }
        self.client.post(reverse('users:register'), data=register_data)
        self.client.post(reverse('users:login'), data=login_data)


    def test_converter(self):
        response = self.client.post(reverse('converter:converter'), data={
            'hryvnias_amount': '100',
            'currency': 'USD'
        })
        
        self.assertContains(
            response,
            text="100 UAH = 2.39 USD"
        )

