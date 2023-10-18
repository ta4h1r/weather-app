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
    print(json.loads(weather))

    # feels like in range -> carry jacket, take a swim, stay in bed,
    # high temp fluctutation -> carry a jacket

    # Use GPT to make hundreds of variations for your dictionaries
    return 0


def get_weather_for_city(city):
    url = BASE_URL + "weather?" + "appid=" + API_KEY + "&q=" + city
    print(url)
    return json.dumps(requests.get(url).json())


def convert_to_unit(temp, unit):
    # TODO
    return temp


def store_weather_data(weather, unit):
    get_weather_recommendation(weather)
    w = json.loads(weather)
    new_weather_item = WeatherItem(**{
        "timestamp": w["dt"],
        "city": w["name"],
        "recommendation": {
            # TODO
        },
        "weather": {
            "temperature": {
                "value": convert_to_unit(w["main"]["temp"], unit),
                "unit": unit
            }
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
