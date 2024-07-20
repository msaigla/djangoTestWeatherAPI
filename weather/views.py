import codecs
import openmeteo_requests
import requests_cache
import pandas as pd
import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from retry_requests import retry
from djangoTestWeatherAPI.settings import BASE_DIR

from django.db.models import Q
from .models import City, WeatherSearchHistory


def index(request):
    print(str(BASE_DIR) + '/djangoTestWeatherAPI/static/countries.json')
    with open(str(BASE_DIR) + '/djangoTestWeatherAPI/static/countries.json', 'r') as f:
        countries = json.load(f)
    data = {
        'title': 'Магазин',
        'countries': countries,
        'searched_cities': City.objects.order_by('-count'),
    }
    return render(request, 'weather/index.html', context=data)


def get_cities(request):
    print("ok1")
    if request.GET:
        print("ok2")
        print(request.GET['text'])
        print(str(BASE_DIR) + '/djangoTestWeatherAPI/static/cities.json')
        with codecs.open(str(BASE_DIR) + '/djangoTestWeatherAPI/static/cities.json', 'r', "utf_8") as f:
            values = json.load(f)
        cities = []
        for id_city, city in enumerate(values):
            if city["country"] == request.GET['text']:
                cities.append(
                    {
                        "name": city["name"],
                        "id": id_city
                    }
                )
    else:
        cities = None
    return JsonResponse({"cities": cities}, status=200)


def get_weather(request):
    if request.GET:
        with codecs.open(str(BASE_DIR) + '/djangoTestWeatherAPI/static/cities.json', 'r', "utf_8") as f:
            values = json.load(f)

            val = values[int(request.GET["id"])]
            if request.user.is_authenticated:
                wsh = WeatherSearchHistory.objects.create(
                    user=request.user,
                    name=val['name'],
                    country=request.GET["country"]
                )
                wsh.save()
            else:
                wsh = []
            try:
                city = City.objects.get(name=val['name'], country=request.GET["country"])
                city.count = city.count + 1
                city.save()
            except:
                city = City.objects.create(name=val['name'], country=request.GET["country"], count=1)
                city.save()
            cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
            retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
            openmeteo = openmeteo_requests.Client(session=retry_session)

            # Make sure all required weather variables are listed here
            # The order of variables in hourly or daily is important to assign them correctly below
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": float(val["lat"]),
                "longitude": float(val["lng"]),
                "current": ["temperature_2m", "relative_humidity_2m", "rain", "wind_speed_10m"],
                "hourly": "temperature_2m",
                "forecast_days": 1
            }

            responses = openmeteo.weather_api(url, params=params)

            response = responses[0]

            # Current values. The order of variables needs to be the same as requested.
            current = response.Current()
            current_temperature_2m = current.Variables(0).Value()
            current_relative_humidity_2m = current.Variables(1).Value()
            current_rain = current.Variables(2).Value()
            current_wind_speed_10m = current.Variables(3).Value()
            text = f"Current time {current.Time()}<br>" \
                   f"Current temperature_2m {current_temperature_2m}<br>" \
                   f"Current relative_humidity_2m {current_relative_humidity_2m}<br>" \
                   f"Current rain {current_rain}<br>" \
                   f"Current wind_speed_10m {current_wind_speed_10m}<br>"

            hourly = response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

            hourly_data = {"date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ), "temperature_2m": hourly_temperature_2m}

            weather = pd.DataFrame(data=hourly_data)

    else:
        weather = []
    return JsonResponse({
        "weather":
            str(weather)
            .replace('date', 'Дата')
            .replace('temperature_2m', 'Температура ℃')
            .replace('\n', '<br>'),
    }, status=200)


def get_history_user_weather(request):
    huw = []
    if request.GET:
        try:
            huw = WeatherSearchHistory.objects.filter(
                user__username=request.GET['username']
            ).order_by('-id').values()
            return JsonResponse({'histories': list(huw)}, status=200)
        except:
            return JsonResponse({'histories': huw}, status=200)
    return JsonResponse({'histories': huw}, status=200)


def count_search_city(request):
    return JsonResponse({'cities': list(City.objects.order_by('-count').values())}, status=200)


