from django.shortcuts import render
from django.core.exceptions import PermissionDenied
import requests

from converter.forms import ConverterForm
from converter.models import ConverterHistory


def get_currency_rate(currency):
    all_rates = requests.get(
        url='https://bank.gov.ua/NBUStatService/v1/statdirectory/' \
        'exchange?json',
    ).json()
    rate = next((cur for cur in all_rates if cur['cc'] == currency), None)
    return rate['rate']


def converter_view(request):
    if request.user.is_anonymous:
        raise PermissionDenied()
    hryvnias_amount, result, currency = None, None, None

    if request.method == 'POST':
        currency = request.POST['currency']
        rate = get_currency_rate(currency)
        hryvnias_amount = request.POST['hryvnias_amount']
        result = round(float(hryvnias_amount) / float(rate), 2)

        convert_in_history = ConverterHistory(
            uah_amount=hryvnias_amount,
            converted_value=result,
            converted_currency=currency,
            rate=rate,
            user_id=request.user
        )
        convert_in_history.save()
        
    converter_form = ConverterForm()

    return render(
        request, 
        'converter/converter.html', 
        {'form': converter_form, 
         'result': result, 
         'currency': currency,
         'hryvnias_amount': hryvnias_amount}
    )


def convert_history_view(request):
    if request.user.is_anonymous:
        raise PermissionDenied()
    history = ConverterHistory.objects.all().filter(
        user_id=request.user.id).order_by('-pk')
    
    return render(request, 'converter/history.html', {'history': history})