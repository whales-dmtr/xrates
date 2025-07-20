from django.test import TestCase
from unittest.mock import MagicMock, patch
from django.http import QueryDict
from django.contrib.auth.models import User

from converter.views import converter_view
from rates.tests.unit.test_rates import all_rates


class ConverterTest(TestCase):
    @patch('converter.views.ConverterHistory')
    @patch('rates.views.cache.get')
    @patch('converter.views.get_rates_from_api')
    def test_converter(
            self, get_rates, get_rates_from_cache, converts_history):
        mocked_request = MagicMock()
        mocked_request.method = 'POST'
        mocked_request.POST = QueryDict('hryvnias_amount=100&currency=USD')
        mocked_request.user = User()
        converts_history.return_value = MagicMock()

        get_rates.return_value = all_rates
        get_rates_from_cache.return_value = None
        
        response = converter_view(mocked_request)

        self.assertContains(response, '100 UAH = 2.4 USD')