from django.shortcuts import render
import requests
from django.core.cache import cache


def rates_view(request):
    rates = cache.get('rates')
    if rates is None:
        all_rates = requests.get(
            url='https://bank.gov.ua/NBUStatService/v1/statdirectory/' \
            'exchange?json',
        ).json()

        currencies = {'USD', 'EUR', 'PLN', 'GBP', 'CHF', 'JPY', 'CZK'}
        rates = [rate for rate in all_rates if rate['cc'] in currencies]
        
        cache.set('rates', rates, 60 * 10)

    return render(request, 'rates/rates.html', {'rates': rates})
