import streamlit as st

# Config
st.set_page_config(page_title="chkscription", layout="centered")

# Admin credentials: NEED TO BE SECURED
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "temppassword"

# Frontend sections
def prescription_verification():
    st.title("Prescription Verification")
    prescription_number = st.text_input("Prescription Number")
    data = st.file_uploader("Upload a QR")
    st.button("Submit")
    # Add fields here

def doctor_portal():
    st.title("Doctor's Portal")

    # Admin authentication
    username = st.text_input("Username", type="default")
    password = st.text_input("Password", type="password")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        if 'medicine_count' not in st.session_state:
            st.session_state.medicine_count = 1
        def add_medicine():
            st.session_state.medicine_count+=1

        patient_name = st.text_input("Name")
        patient_age = st.text_input("Age")
        gender_choice = st.radio("Gender",["male", "female", "other"])
        patient_weight = st.number_input("Weight", 0 , 200)
        patient_allergies = st.text_input("Allergies")
        #drug information
        clicked = st.button("Add medicine", on_click = add_medicine)
        for i in range (1,st.session_state.medicine_count):
            st.text_input(f"Name of the drug {i}", key = f"medicine_name_{i}")
            st.text_input(f"Dosage in mg {i}", key = f"medicine_dosage_{i}")
            st.text_input(f"Frequency of the drug {i}", key = f"medicine_frequency_{i}")
            st.text_input(f"Any Special Instructions {i}", key = f"medicine_instructions_{i}")
        st.button("Submit")
        # add more fields here
    elif username and password:
        st.error("Invalid username or password")

# Sidebar navigation
pages = {
    "Prescription Verification": prescription_verification,
    "Doctor's Portal": doctor_portal,
}

st.sidebar.title("OUTLINE")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Call the selected page function
pages[selection]()



