import json

from flask import Flask, request, jsonify
import requests, datetime
import dateutil.parser as datetime_parser
from geopy.geocoders import Nominatim
from os import getenv

app = Flask(__name__)

geolocation = Nominatim(user_agent="SlyMercymain-tyap-lyap-app")


@app.route("/v1/current/")
def get_current_temperature():
    city = request.args.get("city")
    if city is None:
        return jsonify({"Incorrect parameter": "City parameter is empty"})

    coordinates = geolocation.geocode(city)
    if coordinates is None:
        return jsonify({"Incorrect parameter": "City parameter does not represent city name"})

    reqStr = getenv("API") + "?latitude=" + str(coordinates.latitude) + "&longitude=" + str(
        coordinates.longitude) + "&current_weather=true"

    response = requests.get(reqStr, request=20)
    if response.status_code != 200:
        return jsonify({"Incorrect request": "Something went wrong while getting response from weather API"})

    json_response = response.json()

    return jsonify({"city": city, "temperature": json_response["current_weather"]["temperature"]})


@app.route("/v1/forecast/")
def get_forecast():
    if request.args.get("dt") is None:
        return jsonify({"Incorrect parameter": "Datetime parameter is empty"})

    try:
        dt = datetime_parser.parse(request.args.get("dt"))
    except datetime_parser._parser.ParserError:
        return jsonify({"Incorrect parameter": "Datetime parameter format is incorrerct. Try something like 2023-02-27T11:00"})

    city = request.args.get("city")
    if city is None:
        return jsonify({"Incorrect parameter": "City parameter is empty"})

    coordinates = geolocation.geocode(city)
    if coordinates is None:
        return jsonify({"Incorrect parameter": "City parameter does not represent city name"})

    reqStr = getenv("API") + "?latitude=" + str(coordinates.latitude) + "&longitude=" + \
             str(coordinates.longitude) + "&start_date=" + str(dt.date()) + "&end_date=" + str(dt.date()) +\
             "&hourly=temperature_2m"

    response = requests.get(reqStr, timeout=20)
    if response.status_code != 200:
        return jsonify({"Incorrect request": "Something went wrong while getting response from weather API"})

    json_response = response.json()

    return jsonify({"city": city, "temperature": json_response["hourly"]["temperature_2m"][dt.hour], "time": dt})


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True, port=getenv("PORT"))
