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
    coordinates = geolocation.geocode(city)
    reqStr = getenv("API") + "?latitude=" + str(coordinates.latitude) + "&longitude=" + str(
        coordinates.longitude) + "&current_weather=true"
    json_response = requests.get(reqStr).json()
    return jsonify({"city": city, "temperature": json_response["current_weather"]["temperature"]})


@app.route("/v1/forecast/")
def get_forecast():
    dt = datetime_parser.parse(request.args.get("dt"))
    city = request.args.get("city")
    coordinates = geolocation.geocode(city)
    reqStr = getenv("API") + "?latitude=" + str(coordinates.latitude) + "&longitude=" + \
             str(coordinates.longitude) + "&start_date=" + str(dt.date()) + "&end_date=" + str(dt.date()) +\
             "&hourly=temperature_2m"
    json_response = requests.get(reqStr).json()
    return jsonify({"city": city, "temperature": json_response["hourly"]["temperature_2m"][dt.hour]})


if __name__ == "__main__":
    app.run(debug=True, port=getenv("PORT"))
