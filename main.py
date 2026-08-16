# main-27.py
"""
task-276-Scheduling to trigger via GitHub
"""
import requests
from twilio.rest import Client
import os

TWILIO_ACCOUNT_SID = os.environ.get("ACCT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
MY_LAT = 4.210484
MY_LNG = 101.975769
MY_API = os.environ.get("OWM_API_KEY")
API_END_POINT = "https://api.openweathermap.org/data/2.5/forecast"

# add the "cnt" parameter o limit the number of items in the response
parameters = {
    "lat": MY_LAT,
    "lon": MY_LNG,
    "appid": MY_API,
    "cnt": 4,
}

response = requests.get(API_END_POINT, params=parameters)
response.raise_for_status()
weather_data = response.json()

# print(weather_data["list"][0]["weather"][0]["id"])
will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_="whatsapp:+14155238886",
        to="whatsapp:+6596690168",
        body="Local-It is going to rain today. Remember to bring an umbrella."
    )

    print(message.body)
    
