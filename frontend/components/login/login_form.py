# frontend/components/login/login_form.py
import streamlit as st

def LoginForm():
    
    # Add login form elements
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    return email, password
 
