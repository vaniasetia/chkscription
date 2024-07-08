import streamlit as st
import requests
import qrcode
import io
from PIL import Image

# Config
st.set_page_config(page_title="chkscription", layout="centered")

# Admin credentials: NEED TO BE SECURED
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "temppassword"

# Frontend sections
def prescription_verification():
    st.title("Prescription Verification")
    prescription_number = st.text_input("Prescription Number")
    if st.button("Submit"):
        response = requests.post("http://localhost:8000/verify-prescription", json={"prescription_number": prescription_number})
        if response.status_code == 200:
            verification_result = response.json()
            if verification_result['is_valid']:
                st.success("Prescription is valid.")
                st.json(verification_result['prescription_details'])
            else:
                st.error("Prescription is invalid.")
        else:
            st.error("Failed to verify prescription.")

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
        medicines = []
        clicked = st.button("Add medicine", on_click=add_medicine)
        for i in range(1, st.session_state.medicine_count):
            medicine_name = st.text_input(f"Name of the drug {i}", key=f"medicine_name_{i}")
            medicine_dosage = st.text_input(f"Dosage in mg {i}", key=f"medicine_dosage_{i}")
            medicine_frequency = st.text_input(f"Frequency of the drug {i}", key=f"medicine_frequency_{i}")
            medicine_instructions = st.text_input(f"Any Special Instructions {i}", key=f"medicine_instructions_{i}")
            medicines.append({
                "name": medicine_name,
                "dosage": medicine_dosage,
                "frequency": medicine_frequency,
                "instructions": medicine_instructions
            })
        if st.button("Submit Prescription"):
            prescription_data = {
                "name": patient_name,
                "age": patient_age,
                "gender": gender_choice,
                "weight": patient_weight,
                "allergies": patient_allergies,
                "medicines": medicines
            }
            response = requests.post("http://localhost:8000/issue-prescription", json=prescription_data)
            if response.status_code == 200:
                st.success("Prescription issued successfully.")
                prescription_info = response.json()
                st.write(f"Prescription Number: {prescription_info['prescription_number']}")
                qr_img = qrcode.make(prescription_info["digital_signature"])
                # convert from PILImage to bytes
                img_byte_arr = io.BytesIO()
                qr_img.save(img_byte_arr, format='PNG')
                qr_img = Image.open(img_byte_arr)
                st.image(qr_img, caption="Digital Signature (QR Code)")
            else:
                st.error("Failed to issue prescription.")
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



