import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get('WEATHER_API_KEY')
api_url = 'https://api.openweathermap.org/data/2.5/onecall'
geocoding_url = 'http://api.openweathermap.org/geo/1.0/direct'


def get_weather(city_name):
    lat, lon = get_lat_lon(city_name)
    response = requests.get(
        api_url, params={'lat': lat, 'lon': lon, 'units': 'metric', 'appid': API_KEY, 'exclude': 'minutely,hourly,daily'}).json()
    return response


def get_lat_lon(city_name):
    response = requests.get(geocoding_url, params={
                            'q': city_name, 'limit': 1, 'appid': API_KEY}).json()
    lat = response[0]['lat']
    lon = response[0]['lon']
    return lat, lon
