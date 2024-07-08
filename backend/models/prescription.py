from typing import Optional
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv("MONGO_URI")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Create a new database and collection
db = client['CHK']

# Make collection called prescriptions
prescription_collection = db['prescriptions']

class Prescription:
    def __init__(self, prescription_number, patient_name, patient_age, gender_choice, patient_weight, patient_allergies, medicine, digital_signature):
        self.patient_name = patient_name
        self.patient_age = patient_age
        self.gender_choice = gender_choice
        self.patient_weight = patient_weight
        self.patient_allergies = patient_allergies
        self.medicine = medicine
        self.digital_signature = digital_signature
        self.prescription_number = prescription_number

    def save(self):
        prescription_data = {
            'prescription_number' : self.prescription_number,
            'name' : self.patient_name,
            'age' : self.patient_age,
            'gender' : self.gender_choice,
            'weight' : self.patient_weight,
            'allergies' : self.patient_allergies,
            'medicine' : self.medicine,
            'digital_signature' : self.digital_signature
        }
        prescription_collection.insert_one(prescription_data)    

    @staticmethod
    def find_by_prescription_number(prescription_number: str) -> Optional['Prescription']:
        prescription_data = prescription_collection.find_one({'prescription_number': prescription_number})
        if prescription_data:
            return Prescription(
                prescription_number=prescription_data['prescription_number'],
                patient_name=prescription_data['name'],
                patient_age=prescription_data['age'],
                gender_choice=prescription_data['gender'],
                patient_weight=prescription_data['weight'],
                patient_allergies=prescription_data['allergies'],
                medicine=prescription_data['medicine'],
                digital_signature=prescription_data['digital_signature']
            )
        return None
