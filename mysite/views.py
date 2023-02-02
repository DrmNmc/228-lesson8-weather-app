import os
from django.shortcuts import render
from django.http import JsonResponse
import requests
from .forms import LocationForm


# Create your views here.
def home(request):
    form = LocationForm()
    return render(request, 'index.html', {'form': form})


def get_forecast(weather_data):
    forecast = weather_data['forecast']['forecastDay']['date']
    forecastDict = {}
    for i in range(5):
        date = forecast[i]['date']
        minTemp = forecast[i]['day']['mintemp_f']
        maxTemp = forecast[i]['day']['maxtemp_f']
        forecastDict[f'date{i}'] = date
        forecastDict[f'minTemp{i}'] = minTemp
        forecastDict[f'maxTemp{i}'] = maxTemp
    return forecastDict


def get_weather(request):
    token = os.environ.get('token')
    ip_address = requests.get('https://api.ipify.org').text
    #if ip_address:
    url = f"http://api.weatherapi.com/v1/forecast.json?key={token}&q={ip_address}&aqi=no&days=5"
    response = requests.get(url)
    weather_data = response.json()
    # else:
    #     city= request.POST['city']
    #     state_code=request.POST['state']
    #     url = f"http://api.weatherapi.com/v1/current.json?key={token}&q={city}, {state_code}&aqi=no&days=5"
    #     #city, country_code?
    #     response = requests.get(url)
    #     weather_data = response.json()
    temperature = weather_data['current']['temp_f']
    forecastDict = get_forecast(weather_data)
    s = "The temp is {} degrees.".format(
         temperature)
    data = {"weather_data": s, "forecastDict": forecastDict}
    return JsonResponse(data)


"""
Make the page look nicer by using Bootstrap or another CSS framework in your template files.
Make the app more customizable by allowing the user to choose their own location if the IP location that we guess is wrong
Make the app more useful by showing the weather forecast along with the current weather. (This data is also available from Open Weather Map).
"""

#original
"""
def get_location_from_ip(ip_address):
    response = requests.get("http://ip-api.com/json/{}".format(ip_address))
    return response.json()

def get_weather_from_ip(request):
  ip_address = request.GET.get("ip")
  location = get_location_from_ip(ip_address)
  city = location.get("city")
  country_code = location.get("countryCode")
  weather_data = get_weather_from_location(city, country_code)
  description = weather_data['weather'][0]['description']
  temperature = weather_data['main']['temp']
  s = "You're in {}, {}. You can expect {} with a temperature of {} degrees".format(city, country_code, description, temperature)
  data = {"weather_data": s}
  return JsonResponse(data)

def get_weather_from_location(city, country_code):
    token = os.environ.get("OPEN_WEATHER_TOKEN")
    url = "https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}".format(
        city, country_code, token)
    response = requests.get(url)
    return response.json()
"""
