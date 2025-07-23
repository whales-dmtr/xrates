from django.urls import reverse

from users.tests.integration.test_login import AuthTestCase
from converter.models import ConverterHistory


class ConverterHistoryTest(AuthTestCase):
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

        self.client.post(reverse('converter:converter'), data={
            'hryvnias_amount': '100',
            'currency': 'USD'
        })
        self.client.post(reverse('converter:converter'), data={
            'hryvnias_amount': '1000',
            'currency': 'PLN'
        })

    def test_converter_history(self):
        self.client.get(reverse('converter:history'))

        self.assertEqual(len(ConverterHistory.objects.all()), 2)
