# This software is designed to automate the renewal process of books at the Regina Public Library.
# It uses Selenium WebDriver to interact with the library's website and perform actions such as logging in, navigating to the 'Due Soon' materials, and clicking the 'Renew' button for each book.
# The software also includes error handling to manage cases where no books are found to be renewed.

import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

RPL_url = "https://www.reginalibrary.ca/"
REQUIRED_ENV_VARS = ("BARCODE", "PASSWORD", "EMAIL", "SENDER_PASSWORD")

elements_to_be_scraped = {
    "Go to Login": "/html/body/div[1]/header/div[1]/nav/div/div[2]/div[2]/div/div[1]/span/button",
    "Username Input": "/html/body/div[1]/header/div[1]/nav/div/div[2]/div[2]/div/div[1]/span/ul/div/li/div/form/div[1]/input",
    "Password Input": "/html/body/div[1]/header/div[1]/nav/div/div[2]/div[2]/div/div[1]/span/ul/div/li/div/form/div[2]/input",
    "Login Button": "/html/body/div[1]/header/div[1]/nav/div/div[2]/div[2]/div/div[1]/span/ul/div/li/div/form/input[1]",
    "'My Account' Button": "/html/body/div[1]/header/div[1]/nav/div/div[2]/div[2]/div/div[1]/span/button",
    "Details for 'Due Soon' materials": "/html/body/div[1]/header/div[1]/nav/div/div[2]/div[2]/div/div[1]/span/div/div[2]/div[6]/div[1]/div[3]/a",
    "Book Name": "/html/body/div[1]/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/a",
    "'Renew' Button": "/html/body/div[1]/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/form/input[1]",
}

SMTP_server = "smtp.gmail.com"


def get_required_env_values():
    missing_vars = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
    if missing_vars:
        raise RuntimeError(
            "Missing required environment variables: "
            + ", ".join(missing_vars)
            + ". Configure them in your environment or GitHub Actions secrets."
        )
    return {name: os.getenv(name) for name in REQUIRED_ENV_VARS}


def build_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")

    if os.getenv("GITHUB_ACTIONS", "").lower() == "true" or os.getenv("CI", "").lower() == "true":
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    return chrome_options


def main():
    env_vars = get_required_env_values()
    barcode = env_vars["BARCODE"]
    password = env_vars["PASSWORD"]
    sender_email = env_vars["EMAIL"]
    sender_password = env_vars["SENDER_PASSWORD"]
    receiver_email = sender_email

    driver = None
    try:
        driver = webdriver.Chrome(options=build_chrome_options())
        driver.get(RPL_url)

        wait = WebDriverWait(driver, 10)

        # Try to log in
        target_1 = wait.until(
            EC.element_to_be_clickable((By.XPATH, elements_to_be_scraped["Go to Login"]))
        )
        target_1.click()

        # Type your uname and password
        target_2 = driver.find_element(By.XPATH, elements_to_be_scraped["Username Input"])
        target_2.send_keys(barcode)
        target_3 = driver.find_element(By.XPATH, elements_to_be_scraped["Password Input"])
        target_3.send_keys(password)
        # Click login
        target_4 = driver.find_element(By.XPATH, elements_to_be_scraped["Login Button"])
        target_4.click()

        # Click 'My Account' button
        target_5 = wait.until(
            EC.element_to_be_clickable((By.XPATH, elements_to_be_scraped["'My Account' Button"]))
        )
        target_5.click()
        # Click 'Due Soon' button
        target_6 = wait.until(
            EC.element_to_be_clickable((By.XPATH, elements_to_be_scraped["Details for 'Due Soon' materials"]))
        )
        target_6.click()

        # Create email message
        msg = EmailMessage()
        msg["Subject"] = "Hello from Python!"
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg.set_content("A book from RPL renewed successfully.")

        with smtplib.SMTP(SMTP_server, 587) as server:
            server.ehlo()  # Identify yourself to the server
            server.starttls()  # Secure the connection
            server.ehlo()  # Re-identify as an encrypted connection

            server.login(sender_email, sender_password)
            # Click 'Renew' button
            while True:
                try:
                    book_name = driver.find_element(By.XPATH, elements_to_be_scraped["Book Name"]).text
                    msg.set_content(f"Book '{book_name}' renewed successfully.")
                    target_7 = wait.until(
                        EC.element_to_be_clickable((By.XPATH, elements_to_be_scraped["'Renew' Button"]))
                    )
                    target_7.click()
                    server.send_message(msg)
                    print("🚀 Email sent successfully!")
                except TimeoutException:
                    msg.set_content("No more books to be renewed today")
                    server.send_message(msg)
                    print("❌ No more books to renew.")
                    break

        print("Task completed")
    except Exception as e:
        print(f"❌ Task failed: {type(e).__name__}: {e}")
        raise
    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    main()
