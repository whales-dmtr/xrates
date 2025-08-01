from decimal import Decimal, ROUND_HALF_UP, getcontext

from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from asgiref.sync import sync_to_async

from converter.forms import ConverterForm
from converter.models import ConverterHistory
from rates.views import aget_rates_from_api


async def aget_currency_rate(currency):
    rates = cache.get('rates')
    if rates is None:
        rates = await aget_rates_from_api()
    rate = next((cur for cur in rates if cur['cc'] == currency))
    return rate['rate']


@login_required
async def converter_view(request):
    hryvnias_amount, result, currency, rate = None, None, None, None

    if request.method == 'POST':
        currency = request.POST['currency']
        rate = await aget_currency_rate(currency)
        hryvnias_amount = request.POST['hryvnias_amount']

        # boiler plate for rounding number
        getcontext().rounding = ROUND_HALF_UP  

        converted_curr = Decimal(hryvnias_amount) / Decimal(rate)
        result = converted_curr.quantize(Decimal('0.01'))

        convert_in_history = ConverterHistory(
            uah_amount=hryvnias_amount,
            converted_value=result,
            converted_currency=currency,
            rate=rate,
            user_id=request.user
        )
        convert_in_history.save()
        
    converter_form = ConverterForm()

    return sync_to_async(render)(
        request, 
        'converter/converter.html', 
        {'form': converter_form, 
         'result': result, 
         'currency': currency,
         'hryvnias_amount': hryvnias_amount,
         'rate': rate}
    )


@login_required
def convert_history_view(request):
    history = ConverterHistory.objects.all().filter(
        user_id=request.user.id).order_by('-pk')
    
    return render(request, 'converter/history.html', {'history': history})