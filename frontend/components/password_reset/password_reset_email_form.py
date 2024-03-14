# frontend/components/password_reset/password_reset_email_form.py
import streamlit as st

def PasswordResetEmailForm():
   
    # Add password reset email form elements
    email = st.text_input("Email")

    return email

