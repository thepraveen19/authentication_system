# services/auth_service.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser
import os, sys

# Load configuration from the INI file
# Directly access the path to the database configuration file
EMAIL_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "email.ini")
config = ConfigParser()
config.read(EMAIL_CONFIG_PATH)

def create_reset_email(receiver_email: str, reset_link: str) -> MIMEMultipart:
    # Create a MIME message
    message = MIMEMultipart()
    message["From"] = config["Credentials"]["sender_email"]
    message["To"] = receiver_email
    message["Subject"] = "Password Reset Request"

    # Add the reset link to the email body
    body = f"Click the following link to reset your password: {reset_link}"
    message.attach(MIMEText(body, "plain"))

    return message

def send_email(server: smtplib.SMTP, receiver_email: str, message: MIMEMultipart):
    # Connect to the SMTP server and send the email
    with server:
        server.starttls()
        server.login(config["Credentials"]["sender_email"], config["Credentials"]["password"])
        server.sendmail(config["Credentials"]["sender_email"], receiver_email, message.as_string())

def send_password_reset_email(receiver_email: str, reset_link: str):
    # Create a MIME message
    email_message = create_reset_email(receiver_email, reset_link)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(config["SMTP"]["server"], int(config["SMTP"]["port"])) as server:
        send_email(server, receiver_email, email_message)


