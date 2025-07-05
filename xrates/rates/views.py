from django.shortcuts import render
import requests


def rates_view(request):
    all_rates = requests.get(
        url='https://bank.gov.ua/NBUStatService/v1/statdirectory/' \
        'exchange?json',
    ).json()

    rates = [
        all_rates[32],  # USD
        all_rates[39],  # EUR
        all_rates[41],  # PLN
        all_rates[31],  # GBP
        all_rates[26],  # CHF
        all_rates[12],  # JPY
        all_rates[5],   # CZK
    ]
    
    return render(request, 'rates/rates.html', {'rates': rates})
