##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.
import os
import datetime as dt
import pandas as pd
import random
import smtplib

MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("MY_PASSWORD")
NOW = dt.datetime.now()
MONTH = NOW.month
DAY = NOW.day
SEARCH_TEXT = "[NAME]"
birthdays = pd.read_csv("birthdays.csv")
birthdays_dict = birthdays.to_dict(orient="records")
current_birthday = {}


for birthday in birthdays_dict:
    current_birthday = birthday
    if current_birthday["month"] == MONTH and current_birthday["day"] == DAY:
        name = current_birthday["name"]
        letter_num = random.randint(1, 3)
        with open(f"letter_templates/letter_{letter_num}.txt", "r", encoding="utf-8") as file:
            old_letter = file.read()
            new_letter = old_letter.replace(SEARCH_TEXT, name)
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=current_birthday["email"],
                                msg=f"Subject: Happy Birthday!\n\n{new_letter}"
            )

