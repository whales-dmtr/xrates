import asyncio

import aiohttp
from django.shortcuts import render
from django.core.cache import cache
from asgiref.sync import sync_to_async

URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'


async def aget_rates_from_api() -> list[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            all_rates = await response.json()
    return all_rates


async def rates_view(request):
    rates = cache.get('rates')
    if rates is None:
        all_rates = await asyncio.create_task(aget_rates_from_api())
        currencies = {'USD', 'EUR', 'PLN', 'GBP', 'CHF', 'JPY', 'CZK'}
        rates = [rate for rate in all_rates if rate['cc'] in currencies]
        
        cache.set('rates', rates, 5)

    is_auth = await sync_to_async(lambda: request.user.is_authenticated)

    return await sync_to_async(render)(request, 'rates/rates.html', {'rates': rates, 'is_auth': is_auth})
