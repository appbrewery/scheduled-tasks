import os
import datetime as dt
import smtplib
import random
import pandas

MY_EMAIL=os.environ.get("MY_EMAIL")
MY_PASSWORD=os.environ.get("MY_PASSWORD")

letter_name_list=["letter_1.txt", "letter_2.txt", "letter_3.txt"]
random_letter=random.choice(letter_name_list)
print(random_letter)

today_datetime=dt.datetime.now()
today_month=today_datetime.month
today_date=today_datetime.day

birthday_data=data=pandas.read_csv("birthdays.csv")
birthday_data_list=birthday_data.to_dict(orient="records")
length=len(birthday_data_list)

for i in range(length):
    if birthday_data_list[i]["month"]==today_month and birthday_data_list[i]["day"]==today_date:
        birthday_person_name=birthday_data_list[i]["name"]
        birthday_person_email=birthday_data_list[i]["email"]

        with open(f"./letter_templates/{random_letter}", "r") as birthday_wish:
            birthday_wish_content = birthday_wish.read()
        birthday_wish_content = birthday_wish_content.replace("[NAME]", birthday_person_name)

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=birthday_person_email,
                                msg=f"Subject:Happy Birthday!\n\n{birthday_wish_content}")
