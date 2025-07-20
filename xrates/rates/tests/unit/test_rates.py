from django.test import TestCase
from unittest.mock import patch, MagicMock

from rates.views import rates_view


all_rates = [
    {
        "r030": 840,
        "rate": 41.7514,
        "cc": "USD",
        "exchangedate": "21.07.2025"
    },
    {
        "r030": 978,
        "rate": 48.607,
        "cc": "EUR",
        "exchangedate": "21.07.2025"
    },
    {
        "r030": 985,
        "rate": 11.4397,
        "cc": "PLN",
        "exchangedate": "21.07.2025"
    },
    {
        "r030": 826,
        "rate": 56.1765,
        "cc": "GBP",
        "exchangedate": "21.07.2025"
    },
    {
        "r030": 756,
        "rate": 52.1241,
        "cc": "CHF",
        "exchangedate": "21.07.2025"
    },
    {
        "r030": 392,
        "rate": 0.28112,
        "cc": "JPY",
        "exchangedate": "21.07.2025"
    },
    {
        "r030": 203,
        "rate": 1.9743,
        "cc": "CZK",
        "exchangedate": "21.07.2025"
    },
    {
        "r030": 9991,
        "rate": 123.45,
        "cc": "TEST1",
        "exchangedate": "21.07.2025"
    },
    {
        "r030": 9992,
        "rate": 67.89,
        "cc": "TEST2",
        "exchangedate": "21.07.2025"
    }
]



class RatesTest(TestCase):
    @patch('rates.views.cache.get')
    @patch('rates.views.get_rates_from_api')
    def test_rates(self, get_rates, get_curr_from_cache,):
        get_curr_from_cache.return_value = None
        get_rates.return_value = all_rates
        mocked_request = MagicMock()
        response = rates_view(mocked_request)

        self.assertContains(response, '<tr>', count=8)
