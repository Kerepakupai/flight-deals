import smtplib

import requests
from twilio.rest import Client
import os


TWILIO_SID = os.environ["ENV_TWILIO_SID"]
TWILIO_AUTH_TOKEN = os.environ["ENV_TWILIO_AUTH_TOKEN"]
TWILIO_VIRTUAL_NUMBER = os.environ["ENV_TWILIO_VIRTUAL_NUMBER"]
TWILIO_VERIFIED_NUMBER = os.environ["ENV_TWILIO_VERIFIED_NUMBER"]
MAIL_PROVIDER_SMTP_ADDRESS = "smtp.gmail.com"
MY_EMAIL = os.environ["ENV_MY_EMAIL"]
MY_PASSWORD = os.environ["ENV_MY_PASSWORD"]
TELEGRAM_TOKEN = os.environ["ENV_TELEGRAM_TOKEN"]
TELEGRAM_ENDPOINT = os.environ["ENV_TELEGRAM_ENDPOINT"]
TELEGRAM_CHAT_ID = os.environ["ENV_TELEGRAM_CHAT_ID"]


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)

    @staticmethod
    def send_emails(emails, message, google_flight_link):
        with smtplib.SMTP(MAIL_PROVIDER_SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )

    @staticmethod
    def send_telegram_message(message):
        telegram_params = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        response = requests.get(url=f"{TELEGRAM_ENDPOINT}{TELEGRAM_TOKEN}/sendMessage", params=telegram_params)
        print(response.text)
