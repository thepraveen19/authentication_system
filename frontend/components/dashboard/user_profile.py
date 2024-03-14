# frontend/components/dashboard/user_profile.py
import streamlit as st

def UserProfile(user):
    st.header("User Profile")

    # Display user information
    st.subheader("Personal Information")
    st.write(f"Full Name: {user.full_name}")
    st.write(f"Email: {user.email}")
    st.write(f"Phone Number: {user.phone_number}")

    st.subheader("Additional Information")
    st.write(f"Role: {user.role.role_name}")
    st.write(f"Location: {user.location}")
    st.write(f"Date of Birth: {user.date_of_birth}")
    st.write(f"Avatar: {user.avatar}")
    st.write(f"Bio: {user.bio}")
    st.write(f"Created At: {user.created_at}")
    st.write(f"Last Login: {user.last_login}")
    st.write(f"Updated At: {user.updated_at}")
    st.write(f"Is Active: {user.is_active}")
    st.write(f"Is Superuser: {user.is_superuser}")
    st.write(f"Email Verified: {user.email_verified}")
    st.write(f"Phone Verified: {user.phone_verified}")

    # Add more fields as needed

# End of user_profile.py
