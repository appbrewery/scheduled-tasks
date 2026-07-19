# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


import datetime as dt
import pandas
import random
import smtplib
import os

# import os and use it to get the Github repository secrets
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

data = pandas.read_csv("birthdays.csv")

date = dt.datetime.now()
month = date.month
day = date.day

birthday_dict = {(data_row.month,data_row.day):data_row for (new,data_row) in data.iterrows()}
if (month,day) in birthday_dict:
    birthday_person = birthday_dict[(month,day)]
    with open(f"letter_templates/letter_{random.randint(1,3)}.txt") as f:
        letter_template = f.read()
        n = letter_template.replace("[NAME]",birthday_person["name"])
        print(n)

    with smtplib.SMTP("smtp.gmail.com",587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL,MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,to_addrs=birthday_person["email"],msg=f"Subject: Happy Birthday!\n\n{n}")

