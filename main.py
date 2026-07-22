import os
import requests
from twilio.rest import Client

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
OWM_API_KEY = os.environ.get("OWM_API_KEY")
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
weather_params = {
    "lat"   :   19.075983,
    "lon"   :   72.877655,
    "appid" :   OWM_API_KEY,
    "cnt"   :   4
}
response = requests.get(url=OWM_Endpoint, params=weather_params)
print(response.status_code)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
        print(will_rain)

if will_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        from_='+12603006548',
        body="It's going to rain 🌧️ today. Remember to bring an ☔️",
        to='+919962025865'
    )
    print(message.sid)

