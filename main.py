import os
import requests
from twilio.rest import Client 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("OWM_API_KEY") 
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

params = {#26.7606
    "lat":20.0019,
    "lon":86.2014,  #83.3732
    "appid": api_key,
    "cnt": 4
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=params) 
response.raise_for_status()
weather_data=response.json()

will_rain=False
for i in range(4):
    weather_id=weather_data["list"][i]["weather"][0]["id"]
    if weather_id<700:
        will_rain=True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_="whatsapp:+14155238886",
    body="It's going to rain today. Remember to bring an umbrella",
    to="whatsapp:+919214552029"
    )
    print(message.status)


#current call
# http://api.openweathermap.org/geo/1.0/direct?q=Gorakhpur,UP,IN&appid=1254dc332588bf770cbe0985cad8ea15
#5day/3hour
#http://api.openweathermap.org/data/2.5/forecast?lat=26.7606&lon=83.3732&appid=1254dc332588bf770cbe0985cad8ea15
