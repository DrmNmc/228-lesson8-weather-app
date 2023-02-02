from datetime import datetime, timedelta
import os
from django.shortcuts import render
from django.http import JsonResponse
import requests
from .forms import LocationForm


# Create your views here.
def home(request):
    form = LocationForm()
    return render(request, 'index.html', {'form': form})

def get_weekdays(dates):
    weekdays = []
    for date in dates:
        weekdays.append(datetime.strftime(date, '%A'))
    return weekdays

def get_dates_list(num_days):
    today = datetime.today().date()
    dates = [today + timedelta(days=x) for x in range(num_days)]
    return dates


def get_forecast(weather_data):
    forecastDict = {}
    dates = get_dates_list(5)
    weekdays = get_weekdays(dates)

    for i, date in enumerate(dates):
        forecast = weather_data['forecast']['forecastday'][i]
        dateMatch = forecast['date']
        if dateMatch == str(date):
            wkday = weekdays[i]
            minTemp = forecast['day']['mintemp_f']
            maxTemp = forecast['day']['maxtemp_f']
            forecastDict['date'] = dateMatch
            forecastDict[dateMatch] = [wkday, minTemp, maxTemp]
    return forecastDict


def get_weather(request):
    token = os.environ.get('token')
    ip_address = requests.get('https://api.ipify.org').text
    if request.method == "POST":
        city = request.POST.get('city')
        state_code = request.POST.get('state')
        url = f"http://api.weatherapi.com/v1/forecast.json?key={token}&q={city},{state_code}&aqi=no&days=5"
        response = requests.get(url)
        weather_data = response.json()
    else:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={token}&q={ip_address}&aqi=no&days=5"
        response = requests.get(url)
        weather_data = response.json()
    temperature = weather_data['current']['temp_f']
    forecastDict = get_forecast(weather_data)
    s = "The temp is {}°F.".format(
         temperature)
    data = {"forecastDict": forecastDict}
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
