# main-272-sms.py
"""
1. Get lat and lng from latlong.net
2. Make a request to the forecast API using the requests module
3. Print out the HTTP status code that you get back
4. Print the response to the console
5. Copy-paste the response to an online JSON viewer
6. Locate the weather id and description for each forecast
task-272-Add code to send the message via Twilio
"""
import requests
from twilio.rest import Client

TWILIO_ACCOUNT_SID = "ACdefff43a4a2bc41bd67fb1a939b9d21e"
TWILIO_AUTH_TOKEN = "7e326dae2802b0072f19b459259d3ab6"
MY_LAT = 4.210484
MY_LNG = 101.975769
MY_API = "088803bb59c77e395c77dd4c64ef6961"
# MY_API = OWM_API_KEY
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
