# Weather App
A RESTful weather reporting service built using Django and Redis. 

## Features
The microservice offers the following features:
1. Store weather data and a recommendation for a location: 
   + An endpoint that accepts HTTP POST requests. The request body should contain a location and a temperature unit (Celsius or Fahrenheit). On receiving such a request, the service makes a call to the public weather API (OpenWeatherMap), gets and processes the weather data for the location, converts the temperature to the requested unit, generates a personalized recommendation, and stores it in a local Redis database.
2. Retrieve stored weather data and recommendation for a location: 
   - An endpoint accepting HTTP GET requests takes a location as a query parameter. On receiving a request, the service fetches the weather data and a personalized recommendation for the location from the Redis database and returns them in the response.
3. Requests can only be made against authenticated users, using Basic Auth headers: 
   - The default username:password combination is admin:admin. Users can be configured via the Django [admin interface](127.0.0.1:8000/admin) once the stack is running.

See the [API Docs](https://documenter.getpostman.com/view/25169042/2s9YRB1BLc) for details and examples of each endpoint.

## Recommendation algorithm
To generate customized recommendations based on a particular location's weather data, a heuristic approach was used. In this method the "real feel" temperature, wind speed, precipitation, and temperature fluctuation (i.e., the difference between the high and low temperatures) were each categorized according to a value input range. For example, any temperature between 18 and 25 degrees celcius was categorised as "comfortable", while anything above 32 degrees celcius was categorized as "very hot". Thus, each weather data point can be reduced to a heuristic set, e.g., ["very hot", "light wind", "no rain", "no snow", "slight temperature  fluctuation"]. Each heuristic maps (one-to-one) to a string indicating some required action, e.g., "slight temperature fluctuations" maps to "carry a jacket for later". Thus the heuristic set is mapped to a set of string actions, e.g., ["stay in the shade", "enjoy the breeze", None, None, "carry a jacket for later"], which is stripped of None values and concatenated into a sentence. 

The number of heuristics chosen in the current algorithm can provide up to about 300 different recommendations. However, there is obvious room for extension, (1) by using smaller ranges to define more fine-graned heuristics, and (2) by using one-to-many mappings for each heuristic. This would allow for each heuristic to have a larger variety of recommendations, and more importantly, a weighted roulette method can be used on the deciding the more reasonable strings based on other heuristics in the set. 

The foregoing is a solution to an obvious caveat, where the algorithm falls short due to its 1-to-1 mapping, e.g., if the heuristic set was something like ["very cold", "light wind", "no rain", "no snow", "extreme temperature fluctuation"], the recommendation would be aling the lines of "Carry a jacket, and enjoy the breeze" - but we certainly wouldn't "enjoy" any breeze in the cold weather! Hence, there needs to be a one-to-many mapping, such that "light wind" maps to, say, ["enjoy the breeze", ... , "wear an extra layer"]; the left half of the list has strings which relate to a light breeze in _hot_ weather, while the right half has strings relating to a light breeze in _cold_ weather. Then, the weighted roulette algorithm would look at the previous heuristic ("very hot", or "very cold") and set its weight accordingly, to choose a random string from the correct half of the list. 

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



