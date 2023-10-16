The application should 

interact with a public weather API such as OpenWeatherMap or Weatherstack to 
    fetch the weather data, 
    process it according to certain business logic (defined by you), and then 
    provide a personalized recommendation. This recommendation can be anything from a personalized clothing suggestion to a recommended activity, depending on the weather conditions.

The microservice will expose two primary functionalities through RESTful API endpoints:

Store weather data and recommendation for a location: 
    An endpoint accepting HTTP POST requests. The request body will contain a location and a temperature unit (Celsius or Fahrenheit). On receiving such a request, the service should make a call to the public weather API, get and process the weather data for the location, convert the temperature to the requested unit, generate a personalized recommendation, and store it in a local Redis database. The response should include a confirmation that the data and recommendation were stored successfully.
Retrieve stored weather data and recommendation for a location: 
    An endpoint accepting HTTP GET requests that takes a location as a query parameter. On receiving a request, the service should fetch the weather data and personalized recommendation for the location from the Redis database and return them in the response.