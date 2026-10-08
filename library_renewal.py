# This software is designed to automate the renewal process of books at the Regina Public Library.
# It uses Selenium WebDriver to interact with the library's website and perform actions such as logging in, navigating to the 'Due Soon' materials, and clicking the 'Renew' button for each book.
# The software also includes error handling to manage cases where no books are found to be renewed.

import time, os, smtplib
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

RPL_url = "https://www.reginalibrary.ca/myaccount/currently-borrowed/overdue-soon"

barcode = str(os.getenv("BARCODE"))
password = str(os.getenv("PASSWORD"))

elements_to_be_scraped = {
    "Go to Login": "/html/body/div[1]/div[3]/a[1]",
    "Username Input": "/html/body/div[1]/header/div[2]/div/div[2]/div[2]/div/div/li/div/form/div[1]/input",
    "Password Input": "/html/body/div[1]/header/div[2]/div/div[2]/div[2]/div/div/li/div/form/div[2]/input",
    "Login Button": "/html/body/div[1]/header/div[2]/div/div[2]/div[2]/div/div/li/div/form/input[1]",
    "Book Name": "/html/body/div[1]/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/a",
    "'Renew' Button": "/html/body/div[1]/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/form/input[1]"
}

SMTP_server = "smtp.gmail.com"
sender_email = str(os.getenv("EMAIL"))
sender_password = str(os.getenv("SENDER_PASSWORD"))
receiver_email = str(os.getenv("EMAIL"))

driver = webdriver.Chrome()
driver.get(RPL_url)

time.sleep(7)

# Try to log in
target_1 = driver.find_element(By.XPATH, elements_to_be_scraped["Go to Login"])
target_1.click()

# Type your uname and password
target_2 = driver.find_element(By.XPATH, elements_to_be_scraped["Username Input"])
target_2.send_keys(barcode)
target_3 = driver.find_element(By.XPATH, elements_to_be_scraped["Password Input"])
target_3.send_keys(password)
# Click login
target_4 = driver.find_element(By.XPATH, elements_to_be_scraped["Login Button"])
target_4.click()

time.sleep(7)

# Create email message
msg = EmailMessage()
msg["Subject"] = "Hello from Python!"
msg["From"] = sender_email
msg["To"] = receiver_email
msg.set_content("A book from RPL renewed successfully.")
# Send that message
with smtplib.SMTP(SMTP_server, 587) as server:
    server.ehlo()  # Identify yourself to the server
    server.starttls()  # Secure the connection
    server.ehlo()  # Re-identify as an encrypted connection

    server.login(sender_email, sender_password)
    # Click 'Renew' button
    i = 1
    while True:
        try:
            book_name = driver.find_element(By.XPATH, elements_to_be_scraped["Book Name"]).text
            msg.set_content(f"Book '{book_name}' renewed successfully.")
            target_5 = driver.find_element(By.XPATH, elements_to_be_scraped["'Renew' Button"])
            target_5.click()
            server.send_message(msg)
            print("🚀 Email sent successfully!")
            time.sleep(3)
        except NoSuchElementException:
            msg.set_content("No more books to be renewed today")
            server.send_message(msg)
            print("❌ No more books to renew.")
            break
        i += 1

print("Task completed")
time.sleep(5)
driver.quit()


if __name__ == "__main__":
    main()
