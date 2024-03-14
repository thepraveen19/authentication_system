# frontend/components/password_reset/password_reset_form.py
import streamlit as st

def PasswordResetForm():
    # Extract token from the URL
    token = st.experimental_get_query_params().get("token", [""])[0]

    # Add a password input field
    new_password = st.text_input("New Password", type="password")

    return token, new_password

