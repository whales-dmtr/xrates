from django.test import TestCase
from rates.views import get_rates_from_api


class RatesAPITest(TestCase):
    def test_rates_api(self):
        required_currencies = {'USD', 'EUR', 'PLN', 'GBP', 'CHF', 'JPY', 'CZK'}
        all_rates = get_rates_from_api()

        returned_currencies = {rate['cc'] for rate in all_rates}
        missing = required_currencies - returned_currencies

        self.assertFalse(missing, f"Missing currencies: {missing}")