# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.

print("========== MAIN.PY STARTED ==========", flush=True)
# from datetime import datetime
from dotenv import load_dotenv
import datetime as dt
import pandas as pandas
import random
import smtplib
import os

# import os and use it to get the Github repository secrets
# MY_EMAIL = os.environ.get("MY_EMAIL")
# MY_PASSWORD = os.environ.get("MY_PASSWORD")

# today = datetime.now()
# today_tuple = (today.month, today.day)

# data = pandas.read_csv("birthdays.csv")
# birthdays_dict = {(data_row["month"], data_row["day"])                  : data_row for (index, data_row) in data.iterrows()}
# if today_tuple in birthdays_dict:
#     birthday_person = birthdays_dict[today_tuple]
#     file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
#     with open(file_path) as letter_file:
#         contents = letter_file.read()
#         contents = contents.replace("[NAME]", birthday_person["name"])

#     with smtplib.SMTP("YOUR EMAIL PROVIDER SMTP SERVER ADDRESS") as connection:
#         connection.starttls()
#         connection.login(MY_EMAIL, MY_PASSWORD)
#         connection.sendmail(
#             from_addr=MY_EMAIL,
#             to_addrs=birthday_person["email"],
#             msg=f"Subject:Happy Birthday!\n\n{contents}"
#         )

load_dotenv()

gmail_username = os.environ.get("GMAIL_USERNAME")
gmail_password = os.environ.get("GMAIL_PASSWORD")
google_app_password = os.environ.get("GOOGLE_APP_PASSWORD")
yahoo_username = os.environ.get("YAHOO_USERNAME")
yahoo_password_for_sending_email = os.environ.get("YAHOO_PASSWORD_FOR_SENDING_EMAIL")
yahoo_password = os.environ.get("YAHOO_PASSWORD")
gmail_smtp_address = "smtp.gmail.com"
yahoo_smtp_address = "smtp.mail.yahoo.com"
letters = len(os.listdir("letter_templates"))

print("========== BIRTHDAY LOOKUP ==========", flush=True)

with open("birthdays.csv") as bdays:
    birthdays = pandas.read_csv(bdays)
    birthdays_dict = birthdays.to_dict(orient="records")

print("========== MESSAGE LOOKUP ==========", flush=True)

today = dt.datetime.now()
choice = random.randint(1, letters)
letter_chosen = f"letter_templates/letter_{choice}.txt"

print("Today:", today, flush=True)
print("Birthday:", birthdays, flush=True)
# print("Email:", email, flush=True)
print("Letter:", letter_chosen, flush=True)

print("========== BEFORE EMAIL CONDITION ==========", flush=True)
for record in birthdays_dict:
    if record["day"] == today.day and record["month"] == today.month:
        with open(letter_chosen, "r") as text:
            letter = text.read()
            letter_to_send = letter.replace("[NAME]", record["name"])
            email = record["email"]
        print("connecting...", flush=True)
        with smtplib.SMTP(yahoo_smtp_address) as connection:
            connection.starttls()  # makes the connection secure. In case the email gets intercepted no one can read it.
            connection.login(user=yahoo_username, password=yahoo_password_for_sending_email)
            # connection.login(user=yahoo_username, password=yahoo_password)
            print("Sending email...", flush=True)    
            connection.sendmail(
                from_addr=yahoo_username,
                to_addrs=email,
                msg=f"Subject:Happy Birthday! \n\n{letter_to_send}")
            print("Email Sent", flush=True)
