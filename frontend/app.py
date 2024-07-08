import streamlit as st
import requests
import qrcode
import io
from PIL import Image
import numpy as np
import cv2
from pyzbar.pyzbar import decode
from requests.exceptions import ConnectionError, Timeout, HTTPError

# Configuration for the Streamlit page
st.set_page_config(page_title="CheckPrescription", layout="centered")

# Admin credentials (Note: Change these to secure values)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "temppassword"

# Constants
API_URL = "http://localhost:8000/"
VERIFICATION_ENDPOINT = "verify-prescription"
ISSUE_ENDPOINT = "issue-prescription"
QR_CODE_TYPES = ["png", "jpg", "jpeg"]
MIN_WEIGHT = 0
MAX_WEIGHT = 200

def prescription_verification():
    """Function to verify prescription using a QR code."""
    st.title("Prescription Verification")

    # Input fields for prescription number and QR code upload
    prescription_number = st.text_input("Enter Prescription Number")
    uploaded_file = st.file_uploader("Upload Prescription QR Code", type=QR_CODE_TYPES)
    
    if st.button("Verify"):
        # Validate input
        if not uploaded_file or not prescription_number:
            st.error("Both prescription number and QR code are required.")
            return
        
        # Decode QR code
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        decoded_info = decode(image)
        
        if not decoded_info:
            st.error("No QR code detected in the uploaded image.")
            return
        
        digital_signature = decoded_info[0].data.decode("utf-8")
        
        # Verify prescription with backend
        try:
            response = requests.post(API_URL+VERIFICATION_ENDPOINT, json={
                "prescription_number": prescription_number, 
                "digital_signature": digital_signature
            })
            response.raise_for_status()
            data = response.json()
            
            if data["is_valid"]:
                st.success(data["message"])
                display_prescription_details(data["prescription_details"])
            else:
                st.error(data["message"])
        except ConnectionError:
            st.error("Failed to connect to the server.")
        except Timeout:
            st.error("Request timed out.")
        except HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            st.error(f"An error occurred: {err}")

def display_prescription_details(details):
    """Displays prescription details."""
    st.subheader("Prescription Details")
    st.write(f"Name: {details['patient_name']}")
    st.write(f"Age: {details['patient_age']}")
    st.write(f"Gender: {details['gender_choice']}")
    st.write(f"Weight: {details['patient_weight']} kg")
    st.write(f"Allergies: {details['patient_allergies']}")
    st.subheader("Medicines")
    for i, medicine in enumerate(details["medicines"], 1):
        st.write(f"Medicine {i}: {medicine['name']}")
        st.write(f"  Dosage: {medicine['dosage']} mg")
        st.write(f"  Frequency: {medicine['frequency']}")
        st.write(f"  Instructions: {medicine['instructions']}")

def doctor_portal():
    """Function for the doctor's portal to issue prescriptions."""
    st.title("Doctor's Portal")

    # Authentication
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        if 'medicine_count' not in st.session_state:
            st.session_state.medicine_count = 1
        
        patient_info = collect_patient_info()
        if st.button("Issue Prescription"):
            issue_prescription(patient_info)
    elif username and password:
        st.error("Invalid username or password")

def collect_patient_info():
    """Collects patient information and returns it."""
    st.subheader("Patient Information")
    patient_name = st.text_input("Name")
    patient_age = st.text_input("Age")
    gender_choice = st.radio("Gender", ["Male", "Female", "Other"])
    patient_weight = st.number_input("Weight (kg)", MIN_WEIGHT, MAX_WEIGHT)
    patient_allergies = st.text_input("Allergies")
    
    medicines = collect_medicines_info()
    
    return {
        "name": patient_name,
        "age": patient_age,
        "gender": gender_choice,
        "weight": patient_weight,
        "allergies": patient_allergies,
        "medicines": medicines
    }

def collect_medicines_info():
    """Collects information about medicines."""
    st.subheader("Medicines")
    medicines = []
    for i in range(1, st.session_state.medicine_count + 1):
        st.markdown(f"**Medicine {i}**")
        medicine_name = st.text_input(f"Name", key=f"medicine_name_{i}")
        medicine_dosage = st.text_input(f"Dosage (mg)", key=f"medicine_dosage_{i}")
        medicine_frequency = st.text_input(f"Frequency", key=f"medicine_frequency_{i}")
        medicine_instructions = st.text_input(f"Instructions", key=f"medicine_instructions_{i}")
        medicines.append({
            "name": medicine_name,
            "dosage": medicine_dosage,
            "frequency": medicine_frequency,
            "instructions": medicine_instructions
        })
    if st.button("Add Another Medicine", key="add_medicine"):
        st.session_state.medicine_count += 1
    return medicines

def issue_prescription(patient_info):
    """Issues a prescription based on patient information."""
    try:
        response = requests.post(API_URL+ISSUE_ENDPOINT, json=patient_info)
        response.raise_for_status()
        prescription_info = response.json()
        st.success("Prescription issued successfully.")
        st.write(f"Prescription Number: {prescription_info['prescription_number']}")
        display_qr_code(prescription_info["digital_signature"])
    except ConnectionError:
        st.error("Failed to connect to the server.")
    except Timeout:
        st.error("Request timed out.")
    except HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")

def display_qr_code(digital_signature):
    """Generates and displays a QR code for the digital signature."""
    qr_img = qrcode.make(digital_signature)
    img_byte_arr = io.BytesIO()
    qr_img.save(img_byte_arr, format='PNG')
    qr_img = Image.open(img_byte_arr)
    st.image(qr_img, caption="Digital Signature QR Code")

# Sidebar navigation for page selection
st.sidebar.title("Navigation")
pages = {
    "Prescription Verification": prescription_verification,
    "Doctor's Portal": doctor_portal,
}
selection = st.sidebar.radio("Select a Page", list(pages.keys()))

# Execute the selected page function
pages[selection]()