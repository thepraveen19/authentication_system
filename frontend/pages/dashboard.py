# frontend/pages/dashboard.py
import streamlit as st
from components.dashboard.dashboard_content import DashboardContent

def Dashboard():
    # st.title("Dashboard Page")
    # st.write("Explore and manage your dashboard.")
    DashboardContent()

if __name__ == "__main__":
    Dashboard()

# End of dashboard.py
