import streamlit as st

# Config
st.set_page_config(page_title="chkscription", layout="centered")

# Admin credentials: NEED TO BE SECURED
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "temppassword"

# Frontend sections
def prescription_verification():
    st.title("Prescription Verification")
    # Add fields here

def doctor_portal():
    st.title("Doctor's Portal")

    # Admin authentication
    username = st.text_input("Username", type="default")
    password = st.text_input("Password", type="password")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        name = st.text_input("Name")
        # add more fields here
    elif username and password:
        st.error("Invalid username or password")

# Sidebar navigation
pages = {
    "Prescription Verification": prescription_verification,
    "Doctor's Portal": doctor_portal,
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Call the selected page function
pages[selection]()

