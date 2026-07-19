import os
import requests
from twilio.rest import Client

MY_LAT = 11.843159 # Your latitude
MY_LONG = 13.1536214
API_KEY = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")




parameters = {
    "lat":MY_LAT,
    "lon":MY_LONG,
    "cnt":4,
    "appid":API_KEY,
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast",params=parameters)
response.raise_for_status()

data = response.json()
weather_id = data["list"][0]["weather"][0]["id"]
weather_description = data["list"][0]["weather"][0]["description"]


will_rain = False
for hour_data in data["list"]:
    condition = hour_data["weather"][0]["id"]
    if condition < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_="+16055137544",
        body="Might rain remember to bring an umbrella ☂️!",
        to="+2348034575610"
    )
    print(message.status)

