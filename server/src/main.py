from flask import Flask, jsonify, json, request

from xml.dom import NotFoundErr
from flask import Flask, request
from pydantic import ValidationError
from person import Person
from redis_om import Migrator
from redis_om.model import NotFoundError



app = Flask(__name__)

@app.route('/', methods=['GET'])
def test():
    printTime()
    return jsonify({
        "code": 200,
        "msg": "Hello",
    })


# Create new weather information for location.
@app.route("/weather/new/<location>", methods=["POST"])
def create_weather_info(location):
    try:
        print(request.json)
        new_person = Person(**request.json)
        new_person.save()
        return new_person.pk

    except ValidationError as e:
        print(e)
        return "Bad request.", 400




# Store weather data and recommendation for a location
@app.route('/weather', methods=['POST'])
def post_weather():
    printTime()
    req = request.get_json(force=True)
    db.create()
    return jsonify({
        "code": 200,
        "msg": "Weather",
    })


def main():
    app.run(host="0.0.0.0", port=5001, debug=True)    

if __name__ == "__main__": 
    main()