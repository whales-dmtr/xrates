from django.test import TestCase
from django.urls import reverse


class RatesTest(TestCase):
    def test_rates(self):
        response = self.client.get(reverse('rates'))
        self.assertContains(response, '<tr>', count=8)
