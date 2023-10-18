from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from pydantic import ValidationError

from redis_om.model import NotFoundError
from redis_om import Migrator

from .models import Weather

import json
    
Migrator().run() 

def build_results(entity):
    results = []
    for item in entity:
        results.append(item.dict())
    return results


def get_recommendation(weather_item): 
    # recommendation = new Recommendation(weather_item)
    # return recommendation
    return 0
    

def index(request): 
    try:     
        city = request.GET.get('city')
        
        if(city == None): 
            raise NotFoundError
        
        w = build_results(
            Weather.find(
                (Weather.city == "Lusaka")
            ).all()
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
    if(request.method == "GET"): 
        return HttpResponse("Moron alert method")
    
    content_type = request.META.get('HTTP_CONTENT_TYPE', request.META.get('CONTENT_TYPE'))
    if (content_type != "application/json"):
        return HttpResponse("Moron alert content")
    req_body = json.loads(request.body)
    try:
        new_person = Weather(**req_body)
        new_person.save()
        return HttpResponse(new_person.pk)
    except ValidationError as e:
        print(e)
        HttpResponse.status_code = 400
        return HttpResponse("Bad request")


