import os
import smtplib
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MY_LAT = 41.878113  # Your latitude
MY_LONG = -87.629799  # Your longitude

MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("MY_PASSWORD")
PERSONAL = os.environ.get("REGULAR_EMAIL")

iss_latitude = 0.0
iss_longitude = 0.0
sunrise_dt = None
sunset_dt = None


def get_session_with_retries():
    """Create a requests session with automatic retry logic."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


# Your position is within +5 or -5 degrees of the ISS position.
def iss_is_close():
    close_lat = MY_LAT - 5 <= iss_latitude <= MY_LAT + 5
    close_long = MY_LONG - 5 <= iss_longitude <= MY_LONG + 5
    return close_lat and close_long


def is_dark():
    if sunrise_dt is None or sunset_dt is None:
        return False

    tzinfo = sunrise_dt.tzinfo or sunset_dt.tzinfo
    if tzinfo is None:
        return False

    now = datetime.now(tzinfo)
    sunrise_today = now.replace(
        hour=sunrise_dt.hour,
        minute=sunrise_dt.minute,
        second=sunrise_dt.second,
        microsecond=sunrise_dt.microsecond,
    )
    sunset_today = now.replace(
        hour=sunset_dt.hour,
        minute=sunset_dt.minute,
        second=sunset_dt.second,
        microsecond=sunset_dt.microsecond,
    )
    return now >= sunset_today or now < sunrise_today


def main():
    global iss_latitude, iss_longitude, sunrise_dt, sunset_dt

    try:
        session = get_session_with_retries()
        response = session.get(url="http://api.open-notify.org/iss-now.json", timeout=10)
        response.raise_for_status()
        data = response.json()

        iss_latitude = float(data["iss_position"]["latitude"])
        iss_longitude = float(data["iss_position"]["longitude"])
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        print(f"Error: Could not connect to ISS API after retries: {e}")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch ISS data: {e}")
        return

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
        "tzid": "America/Chicago",
    }

    try:
        response = session.get("https://api.sunrise-sunset.org/json", params=parameters, timeout=10)
        response.raise_for_status()
        data = response.json()
        sunrise_dt = datetime.fromisoformat(data["results"]["sunrise"])
        sunset_dt = datetime.fromisoformat(data["results"]["sunset"])
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        print(f"Error: Could not connect to Sunrise-Sunset API after retries: {e}")
        return
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        print(f"Error: Failed to fetch sunrise-sunset data: {e}")
        return

    # If the ISS is close to my current position
    # and it is currently dark,
    # then send me an email to tell me to look up.
    # if iss_is_close() and is_dark():
    if True:  # TEMP: forcing email test
        try:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(**{"user": MY_EMAIL, "password": PASSWORD})
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=PERSONAL,
                    msg="Subject:ISS IS OVERHEAD\n\nISS is overhead! See if you can spot it!",
                )
            print("Email sent successfully!")
        except smtplib.SMTPException as e:
            print(f"Error: Failed to send email: {e}")
            raise SystemExit(1)
    else:
        print("ISS is not close or it's not dark yet.")


if __name__ == "__main__":
    main()
