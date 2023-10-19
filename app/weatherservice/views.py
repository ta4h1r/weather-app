import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from pydantic import ValidationError
from redis_om.model import NotFoundError
from redis_om import Migrator

from .models import WeatherItem
from .utils import *

Migrator().run()


def index(request):
    try:
        w = []
        city = request.GET.get('city')
        if (city):
            w = build_results(
                WeatherItem.find(
                    (WeatherItem.city == city)
                )
            )
        else:
            w = build_results(
                WeatherItem.find()
            )
        return JsonResponse(w, safe=False)
    except (NotFoundError) as e:
        HttpResponse.status_code = 404
        return HttpResponse("City not found in database")
    except (ValidationError) as e:
        HttpResponse.status_code = 400
        return HttpResponse("Bad request" + + str(e))
    except (TypeError) as e:
        print(e)
        HttpResponse.status_code = 500
        return HttpResponse("Internal server error: " + str(e))


def get_by_id(request, id):
    if (request.method != "GET"):
        HttpResponse.status_code = 400
        return HttpResponse("Bad request method: Should be GET")
    try:
        w = WeatherItem.get(id).dict()
        if not w:
            raise NotFoundError
        return JsonResponse(w, safe=False)
    except (NotFoundError) as e:
        HttpResponse.status_code = 404
        return HttpResponse("City not found in database")
    except (ValidationError) as e:
        HttpResponse.status_code = 400
        return HttpResponse("Bad request" + str(e))
    except (TypeError) as e:
        HttpResponse.status_code = 500
        return HttpResponse("Internal server error: " + str(e))


def get_latest_for_city(request, city):
    try:
        if (request.method != "GET"):
            HttpResponse.status_code = 400
            return HttpResponse("Bad request: Should be GET")
        w = build_results(
            WeatherItem.find(
                (WeatherItem.city == city)
            )
        )
        if w == []:
            raise NotFoundError
        return JsonResponse(w[-1], safe=False)
    except (NotFoundError) as e:
        HttpResponse.status_code = 404
        return HttpResponse("City not found in database")
    except (ValidationError) as e:
        HttpResponse.status_code = 400
        return HttpResponse("Bad request" + str(e))
    except (TypeError) as e:
        print(e)
        HttpResponse.status_code = 500
        return HttpResponse("Internal server error: " + str(e))


@csrf_exempt
def new(request):
    if (request.method != "POST"):
        return HttpResponse("Invalid method: Should be POST")

    if not is_valid_post_request(request):
        HttpResponse.status_code = 404
        return HttpResponse("Bad request: Invalid body")

    try:
        req_body = json.loads(request.body)
        city = req_body["city"]
        temperature_unit = req_body["unit"]
        if (city == None):
            raise NotFoundError

        stored_weather_data = store_weather_data(
            get_weather_for_city(city),
            temperature_unit
        )
        return JsonResponse(
            {
                "message": "Successfully stored weather data and recommendation",
                "data": {
                    "id": stored_weather_data["pk"],
                    "timestamp": stored_weather_data["timestamp"],
                    "city": stored_weather_data["city"]
                }
            }, safe=False
        )
    except ValidationError as e:
        HttpResponse.status_code = 400
        return HttpResponse("Bad request" + str(e))
    except (NotFoundError) as e:
        HttpResponse.status_code = 404
        return HttpResponse("Not found" + str(e))
