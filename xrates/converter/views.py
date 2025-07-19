from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.decorators import login_required

from converter.forms import ConverterForm
from converter.models import ConverterHistory
from rates.views import get_rates_from_api


def get_currency_rate(currency):
    rates = cache.get('rates')
    if rates is None:
        rates = get_rates_from_api()
    rate = next((cur for cur in rates if cur['cc'] == currency))
    return rate['rate']


@login_required
def converter_view(request):
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


@login_required
def convert_history_view(request):
    history = ConverterHistory.objects.all().filter(
        user_id=request.user.id).order_by('-pk')
    
    return render(request, 'converter/history.html', {'history': history})