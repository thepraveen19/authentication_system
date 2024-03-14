import streamlit as st

# Main Streamlit app
def main():
    # Get token from URL parameters
    query_params = st.query_params
    token = query_params.get("token", "")

    # Check if token exists
    if token:
        # Redirect to frontend URL with the token
        frontend_url = "http://0.0.0.0:8501/reset-password?token=" + token
        st.markdown(f"Redirecting to frontend... [Click here to redirect]({frontend_url})")
    else:
        st.error("No token provided.")

if __name__ == "__main__":
    main()
