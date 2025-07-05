from django.shortcuts import render
import requests


def rates_view(request):
    all_rates = requests.get(
        url='https://bank.gov.ua/NBUStatService/v1/statdirectory/' \
        'exchange?json',
    ).json()

    rates = {
        'USD': all_rates[32],
        'EUR': all_rates[39],
        'PLN': all_rates[41],
        'GBP': all_rates[31],
        'CHF': all_rates[26],
        'JPY': all_rates[12],
        'CZK': all_rates[5],
    }
    
    return render(request, 'rates/rates.html', {'rates': list(rates.values())})
