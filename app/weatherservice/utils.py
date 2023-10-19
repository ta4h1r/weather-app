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


def build_recommended_action_string(combination):
    c = [x for x in combination[-5:] if x is not None]
    action = ""
    count = 0
    for str in c: 
        if count == 0 and count != len(c) - 1: 
            action += str + ", "
            count += 1
            continue
        elif count == 0 and count == len(c) - 1:
            action += str + "."
            count += 1
            break
        elif count == len(c) - 1:
            action += "and " + str.lower() + "."
            count = 0
            break
        action += str.lower() + ", "
        count += 1
    return action


def get_weather_recommendation(weather):
    heuristics = calculate_heuristics(weather)
    return build_recommended_action_string(get_combo(heuristics))


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
            "rain": ("N/A" if "rain" not in w else w["rain"]["1h"] if "3h" not in w["rain"] else w["rain"]["3h"]),
            "snow": ("N/A" if "snow" not in w else w["snow"]["1h"] if "3h" not in w["snow"] else w["snow"]["3h"])
        }
    })
    new_weather_item.save()
    return new_weather_item.dict()


def is_valid_post_request(request):
    try: 
        template = {
            "city": str
        }
        if (not request.body):
            return False
        for key, value in template.items():
            if type(json.loads(request.body)[key]) != value:
                return False
        return True
    except (KeyError): 
        return False
