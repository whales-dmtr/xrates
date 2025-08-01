import httpx
from django.shortcuts import render
from django.core.cache import cache
from asgiref.sync import sync_to_async

URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'


async def aget_rates_from_api() -> list[dict]:
    async with httpx.AsyncClient() as client:
        all_rates = await client.get(URL)
    return all_rates.json()


async def rates_view(request):
    rates = cache.get('rates')
    if rates is None:
        all_rates = await aget_rates_from_api()
        currencies = {'USD', 'EUR', 'PLN', 'GBP', 'CHF', 'JPY', 'CZK'}
        rates = [rate for rate in all_rates if rate['cc'] in currencies]
        
        cache.set('rates', rates, 60 * 10)

    sync_to_async(lambda: request.user.is_authenticated)

    return await sync_to_async(render)(request, 'rates/rates.html', {'rates': rates})
