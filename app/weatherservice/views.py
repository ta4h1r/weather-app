import json, os, requests, base64

from django import forms
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from pydantic import ValidationError

from redis_om.model import NotFoundError
from redis_om import Migrator

from .models import WeatherItem
    
Migrator().run() 

API_KEY = os.environ.get('API_KEY', '')
BASE_URL = "http://api.openweathermap.org/data/2.5/"

def build_results(entity):
    results = []
    for item in entity:
        results.append(item.dict())
    return results


def get_weather_recommendation(weather): 
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
    return json.dumps( requests.get(url).json() )

def convertToUnit(temp, unit): 
    return temp

def store_weather_recommendation(weather, unit): 
    get_weather_recommendation(weather)
    # print (weather["dt"])
    # new_weather_item = WeatherItem(**{
    #     "timestamp": weather["dt"],
    #     "city": weather["name"], 
    #     "recommendation": {

    #     }, 
    #     "weather": {
    #         "temperature": convertToUnit(weather["main"]["temp"], unit), 
    #         "unit": unit, 
    #     }
    # })
    # new_person = Weather(**req_body)
        # new_person.save()
        # return HttpResponse(new_person.pk)
    return weather


def index(request): 
    try:     
        city = request.GET.get('city')
        if(city == None): 
            raise NotFoundError
        
        w = build_results(
            WeatherItem.find(
                (WeatherItem.city == city)
            )
        )
        res = json.dumps((w))

        return HttpResponse(res)
    except (NotFoundError) as e:
        HttpResponse.status_code = 404
        return HttpResponse("City not found.")
    except (ValidationError) as e:
        HttpResponse.status_code = 400
        return HttpResponse("Bad request")
    except (TypeError) as e:
        print(e)
        HttpResponse.status_code = 500
        return HttpResponse("Internal server error: " + str(e))

@csrf_exempt
def new(request):
    if(request.method != "POST"): 
        return HttpResponse("Invalid method")   

    if not is_valid_post_request(request):
        HttpResponse.status_code = 404
        return HttpResponse("Bad request")
    
    try:    
        req_body = json.loads(request.body)
        city = req_body["city"]
        temperature_unit = req_body["unit"]
        if(city == None): 
            raise NotFoundError
        
        return HttpResponse(
            store_weather_recommendation(
                get_weather_for_city(city), 
                temperature_unit
            )
        )
    except ValidationError as e:
        print(e)
        HttpResponse.status_code = 400
        return HttpResponse("Bad request")
    except (NotFoundError) as e:
        HttpResponse.status_code = 404
        return HttpResponse("Not found.")


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