# frontend/pages/password_reset_page.py
import streamlit as st
import requests
from components.password_reset.password_reset_form import PasswordResetForm  # Add your password reset form component
import json

# Load configuration from config.json
with open("/home/xbot/Eq_Algo_Project/Authentication_system/frontend/config/config.json", "r") as config_file:
    config = json.load(config_file)

# Extract backend URL from the configuration
backend_url = config.get("backend_url", "http://127.0.0.1:8000")
frontend_url = config.get("frontend_url", "http://0.0.0.0:8501")

st.title("Password Reset")
PasswordResetForm()


    