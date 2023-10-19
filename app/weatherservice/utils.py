import json
import requests
import os
from .models import WeatherItem

API_KEY = os.environ.get('API_KEY', '')
BASE_URL = "http://api.openweathermap.org/data/2.5/"


def build_results(entity):
    results = []
    for item in entity:
        results.append(item.dict())
    return results


def get_weather_recommendation(weather):
    # TODO
    # recommendation = new Recommendation(weather_item)
    # return recommendation
    # print(json.loads(weather))

    # feels like in range -> carry jacket, take a swim, stay in bed,
    # high temp fluctutation -> carry a jacket

    # Use GPT to make hundreds of variations for your dictionaries
    return {
        "actions": "Go away",
        "clothing": "Kimono"
    }


def get_weather_for_city(city):
    url = BASE_URL + "weather?" + "appid=" + API_KEY + "&q=" + city
    print(url)
    return json.dumps(requests.get(url).json())


def to_celcius(temp):
    kelvin_temp = temp
    celcius_temp = kelvin_temp - 273.15
    return celcius_temp


def to_farenheit(temp):
    kelvin_temp = temp
    celcius_temp = to_celcius(kelvin_temp)
    farenheit_temp = celcius_temp * 9/5 + 32
    return farenheit_temp


def convert_to_unit(temp, unit):
    t = temp
    if (unit.lower() == "farenheit" |
            unit.lower() == "f"):
        t = to_farenheit(temp)
    if (unit.lower() == "celcius" |
            unit.lower() == "c"):
        t = to_celcius(temp)
    return t


def store_weather_data(weather, unit):
    r = get_weather_recommendation(weather)
    w = json.loads(weather)
    new_weather_item = WeatherItem(**{
        "timestamp": w["dt"],
        "city": w["name"],
        "recommendation": r,
        "weather": {
            "temperature": {
                "value": convert_to_unit(w["main"]["temp"], unit),
                "unit": unit
            },
            "wind": {
                "speed": w["wind"]["speed"],
                "direction": w["wind"]["deg"]
            },
            "summary": w["weather"][0]["main"],
            "description": w["weather"][0]["description"],
        }
    })
    new_weather_item.save()
    return new_weather_item.dict()


def is_valid_post_request(request):
    template = {
        "city": str,
        "unit": str
    }
    if (not request.body):
        return False
    for key, value in template.items():
        if type(json.loads(request.body)[key]) != value:
            return False
    return True
