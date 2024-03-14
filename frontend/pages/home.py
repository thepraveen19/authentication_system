# frontend/pages/home.py
import streamlit as st
from st_pages import Page, show_pages, add_page_title
import webbrowser
 

def open_url_in_new_tab(url):
    webbrowser.open_new_tab(url)

def home():
    add_page_title(layout="wide")
    
    show_pages(
        [
            Page("app.py", "Home", "🏠"),
            Page("pages/signup.py", "Sign Up", ":✳️:"),
            Page("pages/login.py", "Login", ":✅:"),
            Page("pages/dashboard.py", "Dashboard", ":💹:"),
            Page("pages/password_reset_email_page.py", "Password Reset", ":🔑:")
        ]
    )
    # Read introduction text from file
    with open("intro.txt", "r", encoding="utf-8") as file:
        introduction_text = file.read()

    # Display the introduction text
    st.write(introduction_text)

    # Define button URLs
    authorize_xbot_url = "https://api-t1.fyers.in/api/v3/generate-authcode?client_id=XHGPGEM27R-102&redirect_uri=xbot.capital&response_type=code&state=None"
    register_url = "https://docs.google.com/forms/d/1XBvOWbKBm2Ui1XeNEAknhRF5QPrLXlJ0hEjivZ0N2EA/viewform?edit_requested=true"

    # Create a layout with two columns
    col1, col2, col3, col4 = st.columns(4)

    # Add space before buttons
    col1.write("")  # Empty space
    col2.write("")  # Empty space
    col3.write("")  # Empty space
    col4.write("")  # Empty space

   # Button 1: Authorize xBot
    if col1.button("Authorize xBot"):
        open_url_in_new_tab(authorize_xbot_url)

    # Button 2: Register
    if col2.button("Register"):
        open_url_in_new_tab(register_url)


if __name__ == "__main__":
    home()

