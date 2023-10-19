import base64
from django.http import HttpResponse
from django.contrib.auth import authenticate


def is_authenticated(username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        return True
    else:
        return False


def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        # Bypass basic auth for admin page
        if ("/admin" in request.path_info):
            return response

        # Code to be executed for each request/response after
        # the view is called.

        # Check auth
        headers = request.headers
        try:
            if (headers['Authorization'].split(" ")[0] != "Basic"):
                HttpResponse.status_code = 403
                return HttpResponse("Auth not supported")
            auth_data = base64.b64decode(headers['Authorization'].split(" ")[
                                         1]).decode().split(":")
            if (not is_authenticated(auth_data[0], auth_data[1])):
                HttpResponse.status_code = 403
                return HttpResponse("Unauthorized")
        except (KeyError) as e:
            return HttpResponse("Invalid auth header")

        return response

    return middleware
