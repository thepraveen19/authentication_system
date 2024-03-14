# frontend/components/signup/signup_form.py
import streamlit as st

def SignupForm():

    # Add signup form elements
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone_number = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    return full_name, email, phone_number, password, confirm_password
