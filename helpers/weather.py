import requests
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

API_KEY = os.environ.get('WEATHER_API_KEY')
api_url = 'https://api.openweathermap.org/data/2.5/onecall'
geocoding_url = 'http://api.openweathermap.org/geo/1.0/direct'

weather_icons = {
    '01d': '☀️',
    '01n': '🌙',
    '02d': '⛅',
    '02n': '⛅',
    '03d': '☁️',
    '03n': '☁️',
    '04d': '☁️',
    '04n': '☁️',
    '09d': '🌧️',
    '09n': '🌧️',
    '10d': '🌦️',
    '10n': '🌦️',
    '11d': '⛈️',
    '11n': '⛈️',
    '13d': '❄️',
    '13n': '❄️',
    '50d': '🌫️',
    '50n': '🌫️',
}


def get_weather(city_name):
    name, lat, lon = get_lat_lon(city_name)
    response = requests.get(
        api_url, params={'lat': lat, 'lon': lon, 'units': 'metric', 'appid': API_KEY, 'exclude': 'minutely,hourly'}).json()
    weather = response['current']['weather'][0]['description']
    weather_icon = weather_icons[response['current']['weather'][0]['icon']]
    temp = response['current']['temp']
    feels_like = response['current']['feels_like']
    humidity = response['current']['humidity']
    wind_speed = response['current']['wind_speed']
    cloud = response['current']['clouds']
    sunrise = datetime.fromtimestamp(
        response['current']['sunrise']).strftime('%H:%M:%S')
    sunset = datetime.fromtimestamp(
        response['current']['sunset']).strftime('%H:%M:%S')
    temp_min = response['daily'][1]['temp']['min']
    temp_max = response['daily'][1]['temp']['max']
    rain = response['daily'][1].get('rain', 0)
    snow = response['daily'][1].get('snow', 0)
    weather_today = f'''<b>{name}, <i>{temp}°C, {weather}</i></b>
➡️ <b>Weather:</b> {weather} {weather_icon}
🌡️ <b>Temperature:</b> {temp}°C (feels like: {feels_like}°C)
🌡️ <b>Temperature (min/max):</b> {temp_min}°C/{temp_max}°C
💧 <b>Humidity:</b> {humidity}%
💨 <b>Wind speed:</b> {wind_speed} metre/sec
☁️ <b>Cloud</b> {cloud}%
☔ <b>Rain:</b> {rain} mm
🌨️ <b>Snow:</b> {snow} mm
🌄 <b>Sunrise:</b> {sunrise}
🌇 <b>Sunset:</b> {sunset}
'''
    return weather_today


def get_lat_lon(city_name):
    response = requests.get(geocoding_url, params={
                            'q': city_name, 'limit': 1, 'appid': API_KEY}).json()
    lat = response[0]['lat']
    lon = response[0]['lon']
    name = response[0]['name']
    return name, lat, lon
