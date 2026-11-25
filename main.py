import requests
import os

URL = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = os.environ.get("OWM_MY_API")

parameters = {
    'lat':23.17,
    'lon':108.44,
    'appid':API_KEY,
    'cnt':4,
    'lang':'zh_cn'
}

response = requests.get(url=URL,params=parameters)
response.raise_for_status()
data = response.json()
will_rain = False
condition_codes = [item["weather"][0]["id"] for item in data["list"]]
for id in condition_codes:
    if int(id) < 700:
        will_rain = True
if will_rain:
    print("Bring an umbrella today!")
