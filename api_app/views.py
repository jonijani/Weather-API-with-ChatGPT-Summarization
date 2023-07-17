from django.shortcuts import render

from scrapping_module.main import get_city_weather_update
import json
from django.http import JsonResponse

def home(request,city,date):
    data = get_city_weather_update(city,date)
    json_data = JsonResponse(data,safe=False)
    return json_data

