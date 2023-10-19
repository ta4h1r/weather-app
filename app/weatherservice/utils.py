import json
import requests
import os
from .models import WeatherItem
from .calculations import get_combo, calculate_heuristics, convert_to_unit

API_KEY = os.environ.get('API_KEY', '')
BASE_URL = "http://api.openweathermap.org/data/2.5/"


def build_results(entity):
    results = []
    for item in entity:
        results.append(item.dict())
    return results


def get_recommended_action(combination):
    c = [x for x in combination[-5:] if x is not None]
    action = ""
    count = 0
    for str in c: 
        if count == 0: 
            action += str + ", "
            count += 1
            continue
        elif count == len(c) - 1:
            action += "and " + str.lower() + "."
            count = 0
            break
        action += str + ", "
        count += 1
    return action


def get_weather_recommendation(weather):
    heuristics = calculate_heuristics(weather)
    return get_recommended_action(get_combo(heuristics))


def get_weather_for_city(city):
    url = BASE_URL + "weather?" + "appid=" + API_KEY + "&q=" + city
    print(url)
    return json.dumps(requests.get(url).json())


def store_weather_data(weather, unit):
    w = json.loads(weather)
    r = get_weather_recommendation(w)
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
        },
        "precipitation": {
            "rain": (w["rain"]["3h"] if "rain" in w else ""),
            "snow": (w["snow"]["3h"] if "snow" in w else "")
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
