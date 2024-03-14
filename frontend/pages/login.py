# frontend/pages/login.py
import streamlit as st
from components.login.login_form import LoginForm
import requests
import json

# Load configuration from config.json
with open("/home/xbot/Eq_Algo_Project/Authentication_system/frontend/config/config.json", "r") as config_file:
    config = json.load(config_file)

# Extract backend URL from the configuration
backend_url = config.get("backend_url", "http://127.0.0.1:8000")
frontend_url = config.get("frontend_url", "http://0.0.0.0:8501")

# Streamlit UI components for user registration
st.title("User Login")

# Get the login form data
email, password = LoginForm()

# Check if the login button is clicked
if st.button("Login"):
    # API endpoint for login
    login_endpoint = f"{backend_url}/login"

    # Prepare the request payload
    payload = {
        "email": email,
        "password": password
    }

    try:
        # Make a POST request to the login endpoint
        response = requests.post(login_endpoint, json=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            st.success("Login successful!")

            # Extract JWT token from the response
            token_data = response.json()
            jwt_token = token_data.get("access_token")

            # You can store the JWT token or perform additional actions here
            # For example, you might want to use the token in future API requests
            # headers = {"Authorization": f"Bearer {jwt_token}"}
            # response = requests.get("http://your-protected-endpoint", headers=headers)
        else:
            st.error(f"Login failed. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred during login: {e}")

# Assuming the URLs for signup and forgot password pages
signup_url = f"{frontend_url}/Sign%20Up"
forgot_password_url = f"{frontend_url}/Password%20Reset"


# Display clickable text to navigate to Sign Up page
st.markdown(f"[New to Xbot? Sign up here.]({signup_url})")

# Display clickable text to navigate to Forgot Password page
st.markdown(f"[Forgot Password?]({forgot_password_url})")
 
