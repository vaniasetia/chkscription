from typing import Optional
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Constants
DATABASE_NAME = 'CHK'
PRESCRIPTIONS_COLLECTION = 'prescriptions'

def get_database():
    """Load environment variables and return a database connection."""
    load_dotenv()
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        return client[DATABASE_NAME]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

db = get_database()

class Prescription:
    """A class to represent a patient's prescription."""
    def __init__(self, prescription_number, patient_name, patient_age, gender_choice, patient_weight, patient_allergies, medicines, digital_signature):
        self.prescription_number = prescription_number
        self.patient_name = patient_name
        self.patient_age = patient_age
        self.gender_choice = gender_choice
        self.patient_weight = patient_weight
        self.patient_allergies = patient_allergies
        self.medicines = medicines
        self.digital_signature = digital_signature

    def save(self):
        """Save the prescription to the database."""
        if db is None:
            print("Database connection not established.")
            return
        prescription_data = {
            'prescription_number': self.prescription_number,
            'name': self.patient_name,
            'age': self.patient_age,
            'gender': self.gender_choice,
            'weight': self.patient_weight,
            'allergies': self.patient_allergies,
            'medicines': self.medicines,
            'digital_signature': self.digital_signature
        }
        db[PRESCRIPTIONS_COLLECTION].insert_one(prescription_data)

    @staticmethod
    def find_by_prescription_number(prescription_number: str) -> Optional['Prescription']:
        """Find a prescription by its number."""
        if db is None:
            print("Database connection not established.")
            return None
        prescription_data = db[PRESCRIPTIONS_COLLECTION].find_one({'prescription_number': prescription_number})
        if prescription_data:
            return Prescription(
                prescription_data['prescription_number'],
                prescription_data['name'],
                prescription_data['age'],
                prescription_data['gender'],
                prescription_data['weight'],
                prescription_data['allergies'],
                prescription_data['medicines'],
                prescription_data['digital_signature'])
        return None