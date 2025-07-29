from decimal import Decimal, ROUND_HALF_UP, getcontext

from django.urls import reverse
from lxml import html

from users.tests.integration.test_login import AuthTestCase


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

        doc = html.fromstring(response.content) 
        current_rate = doc.xpath("//input[@id='rate']/@value")[0]

        # boiler plate for rounding number
        getcontext().rounding = ROUND_HALF_UP  

        expected_result = Decimal(100) / Decimal(current_rate)
        expected_rounded_result = expected_result.quantize(Decimal('0.01'))
        
        self.assertContains(
            response,
            text=f"100 UAH = {expected_rounded_result} USD"
        )

