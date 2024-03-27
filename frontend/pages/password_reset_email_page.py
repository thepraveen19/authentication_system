import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
os.getenv("config_path")

# Load configuration from config.json
config_path = os.getenv("config_path")
# Load configuration from config.json
with open(config_path, "r") as config_file:
    config = json.load(config_file)

# Extract backend URL from the configuration
backend_url = config.get("backend_url", "http://127.0.0.1:8000")

st.title("Password Reset")

# Get the password reset email from the user
email = st.text_input("Enter your email address")

if st.button("Send Reset Email"):
    if not email:
        st.error("Please enter a valid email address.")
    else:
        # Call the backend API to send the password reset email
        api_endpoint = "/forgot-password"
        payload = {"email": email}

        # Make the API request
        response = requests.post(f"{backend_url}{api_endpoint}", json=payload)

        if response.status_code == 200:
            st.success("Password reset instructions sent to your email. Please check your inbox (and spam folder).")
            st.session_state.form_visibility = True

# Display form for secret key and new password if form visibility is True
if "form_visibility" not in st.session_state:
    st.session_state.form_visibility = False

if st.session_state.form_visibility:
    secret_key = st.text_input("Enter the secret key from the email")
    new_password = st.text_input("Enter your new password", type="password")

    if st.button("Reset Password"):
        if not secret_key or not new_password:
            st.warning("Please enter both the secret key and a new password.")
        else:
            # Make the API request
            reset_endpoint = "/reset-password"
            reset_payload = {"key": secret_key, "new_password": new_password}

            # Construct the full URL with the provided key and new password
            url = f"{backend_url}{reset_endpoint}"

            # Make the API request
            reset_response = requests.post(url, params=reset_payload)


            if reset_response.status_code == 200:
                st.success("Password reset successfully.")
            else:
                st.error("Failed to reset password. Please try again later.")
else:
    st.warning("Please enter your email address and click 'Send Reset Email' to receive instructions.")
