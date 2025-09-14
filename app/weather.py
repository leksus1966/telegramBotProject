import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
LANG = os.getenv('LANG', 'ru')
UNITS = os.getenv('UNITS', 'metric')

OW_URL = 'https://api.openweathermap.org/data/2.5/weather'
OW_FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'


async def fetch_weather(city: str):
    return await _fetch(OW_URL, city)


async def fetch_forecast(city: str):
    return await _fetch(OW_FORECAST_URL, city)


async def _fetch(url: str, city: str):
    if not OPENWEATHER_API_KEY:
        raise RuntimeError('OPENWEATHER_API_KEY is not set')
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': UNITS,
        'lang': LANG,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                return await resp.json()
            elif resp.status == 404:
                return {'error': 'city_not_found'}
            else:
                text = await resp.text()
                return {'error': 'api_error', 'status': resp.status, 'text': text}


def parse_weather(data: dict) -> dict:
    weather = data.get('weather', [{}])[0]
    main = data.get('main', {})
    wind = data.get('wind', {})
    sys = data.get('sys', {})

    return {
        'city': data.get('name'),
        'country': sys.get('country'),
        'description': weather.get('description'),
        'icon': weather.get('icon'),
        'temp': main.get('temp'),
        'feels_like': main.get('feels_like'),
        'temp_min': main.get('temp_min'),
        'temp_max': main.get('temp_max'),
        'pressure': main.get('pressure'),
        'humidity': main.get('humidity'),
        'wind_speed': wind.get('speed'),
    }


def parse_forecast(data: dict) -> list:
    result = []
    for item in data.get('list', [])[:5]:  # ближайшие 5 интервалов (~15 часов)
        weather = item.get('weather', [{}])[0]
        main = item.get('main', {})
        result.append({
            'dt_txt': item.get('dt_txt'),
            'description': weather.get('description'),
            'icon': weather.get('icon'),
            'temp': main.get('temp'),
        })
    return result
