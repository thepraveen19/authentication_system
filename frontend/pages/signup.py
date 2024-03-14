import streamlit as st
from components.signup.signup_form import SignupForm
import requests
import json

# Load configuration from config.json
with open("/home/xbot/Eq_Algo_Project/Authentication_system/frontend/config/config.json", "r") as config_file:
    config = json.load(config_file)

# Extract backend URL from the configuration
backend_url = config.get("backend_url", "http://127.0.0.1:8000")

# Streamlit UI components for user registration
st.title("User Registration")

# Include SignupForm component
full_name, email, phone_number, password, confirm_password = SignupForm()

# Register button
if st.button("Register"):
    # Make request to FastAPI endpoint for user registration
    payload = {
        "full_name":full_name ,
        "email": email,
        "phone_number": phone_number,
        "password":password,
    }
    
    response = requests.post(f"{backend_url}/register", json=payload)

    # Display response in Streamlit app
    if response.status_code == 200:
        data = response.json()
        st.success(data.get("message", "User registered successfully"))
    else:
        st.error(f"Error: {response.status_code}")
