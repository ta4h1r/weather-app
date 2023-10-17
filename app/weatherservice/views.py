from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from pydantic import ValidationError
from redis_om.model import NotFoundError

from django.views.decorators.csrf import csrf_exempt

from .models import Person

import json
    

def build_results(people):
    response = []
    for person in people:
        response.append(person.dict())

    return { "results": response }


def find_by_id(id):
    try:
        person = Person.get(id)
        return person.dict()
    except NotFoundError:
        return {}
    


def index(request): 
    id = request.GET.get('id')
    # page = request.GET.get('page', 1)
    return HttpResponse(json.dumps(
        Person.get(id).dict()
    ))

@csrf_exempt
def create(request):
    if(request.method == "GET"): 
        return HttpResponse("Moron alert method")
    
    content_type = request.META.get('HTTP_CONTENT_TYPE', request.META.get('CONTENT_TYPE'))
    if (content_type != "application/json"): 
        return HttpResponse("Moron alert content")
    
    req_body = json.loads(request.body)
    loc = req_body["Location"]
    unit = req_body["Unit"]
    try:
        new_person = Person(**{"location": loc})
        new_person.save()
        return HttpResponse(new_person.pk)
    except ValidationError as e:
        print(e)
        return HttpResponse("Bad request.", 400)


