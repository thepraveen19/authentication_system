# services/auth_service.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser
import os, sys

# Load configuration from the INI file
# Directly access the path to the database configuration file
EMAIL_CONFIG_PATH = '/home/xbot/Eq_Algo_Project/Authentication_system_repo/config/email.ini'
config = ConfigParser()
config.read(EMAIL_CONFIG_PATH)

def create_yellow_email(receiver_email: str) -> MIMEMultipart:
    # Create a MIME message
    message = MIMEMultipart()
    message["From"] = config["Credentials"]["sender_email"]
    message["To"] = receiver_email
    message["Subject"] = "Test Email"

    # Add yellow text to the email body
    body = '<html><body style="background-color: yellow;"><p>Hello, this is a test email with yellow text!</p></body></html>'
    message.attach(MIMEText(body, "html"))

    return message

def send_email(receiver_email: str):
    # Create a MIME message with yellow text
    email_message = create_yellow_email(receiver_email)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(config["SMTP"]["server"], int(config["SMTP"]["port"])) as server:
        # Connect to the SMTP server and send the email
        with server:
            server.starttls()
            server.login(config["Credentials"]["sender_email"], config["Credentials"]["password"])
            server.sendmail(config["Credentials"]["sender_email"], receiver_email, email_message.as_string())

send_email('thepraveen19@gmail.com')