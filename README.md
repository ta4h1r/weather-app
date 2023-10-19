# Weather App
A RESTful weather reporting service built using Django and Redis. 
## Pre-requisties

### Either 
 
1. <a href="https://docs.docker.com/get-docker/">Docker Engine</a> with <a href="https://docs.docker.com/compose/install/">Docker Compose</a>

See <a> https://docs.docker.com/compose/gettingstarted/</a> to get started.

### Or
1. [Python 3.8](https://www.python.org/downloads/)</a> or higher
2. [Redis Stack](https://redis.io/docs/getting-started/install-stack/) database, or Redis with the [Search and Query](https://redis.io/docs/stack/search/) and [JSON](https://redis.io/docs/stack/json/) features installed


## Setup
```
$ cd weather-app && \
    echo "API_KEY=my_api_key" > .env && \
    echo "REDIS_OM_URL=redis://db:6379/" >> .env
```
Where _my_api_key_ is obtained from [OpenWeatherMap](https://openweathermap.org/appid). If you are not using Docker, replace _db_ with _localhost_ in the REDIS_OM_URL.   

## Run using Docker

```
$ docker-compose up -d 
```

## Run without Docker 
###  MacOS and Linux
```
$ redis-stack-server
$ source .env
$ pip install -r requirements.txt 
$ cd app && python manage.py runserver
```
### Windows
See https://redis.io/docs/getting-started/install-stack/windows/ to get the redis stack running. Then run in PowerShell:
```
> pip install -r -requirements.txt
> cd app && python manage.py runserver
```
<h2>Features</h2>
The microservice offers the following features:

1. Store weather data and a recommendation for a location: 
   + An endpoint that accepts HTTP POST requests. The request body should contain a location and a temperature unit (Celsius or Fahrenheit). On receiving such a request, the service makes a call to the public weather API (OpenWeatherMap), gets and processes the weather data for the location, converts the temperature to the requested unit, generates a personalized recommendation, and stores it in a local Redis database.
2. Retrieve stored weather data and recommendation for a location: 
   - An endpoint accepting HTTP GET requests takes a location as a query parameter. On receiving a request, the service fetches the weather data and a personalized recommendation for the location from the Redis database and returns them in the response.
3. Requests can only be made against authenticated users, using Basic Auth headers: 
   - The default username:password combination is admin:admin. Users can be configured via the Django [admin interface](127.0.0.1:8000/admin) once the stack is running.

See the [API Docs](https://documenter.getpostman.com/view/25169042/2s9YRB1BLc) for details and examples of each endpoint.

