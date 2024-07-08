# server.py
from flask import Flask, request, jsonify
from models.prescription import Prescription
from utils.digital_signature import DigitalSignature
import random

private_key = open('keys/private.pem').read()
public_key = open('keys/public.pem').read()

DSGen = DigitalSignature(private_key, public_key)

app = Flask(__name__)

def generate_prescription_number():
    # generate random number of 10 digits
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

# Prescription issuance route (accessible only to admins)
@app.route('/issue-prescription', methods=['POST'])
def issue_prescription():
    data = request.get_json()
    patient_name = data.get('name')
    patient_age = data.get('age')
    medicine = data.get('medicine')
    gender_choice = data.get('gender')
    patient_weight = data.get('weight')
    patient_allergies = data.get('allergies')
    prescription_number = generate_prescription_number()

    digital_signature_str = DSGen.generate_signature(f"{prescription_number}|{patient_name}|{patient_age}|{medicine}|{gender_choice}|{patient_weight}|{patient_allergies}".encode('utf-8'))

    prescription = Prescription(prescription_number, patient_name, patient_age, gender_choice, patient_weight, patient_allergies, medicine, digital_signature_str)
    prescription.save()

    return jsonify({'message': 'prescription issued successfully', 'prescription_number': prescription_number, 'digital_signature': digital_signature_str}), 200


# prescription verification route
@app.route('/verify-prescription', methods=['POST'])
def verify_prescription():
    data = request.get_json()
    prescription_number = data.get('prescription_number')
    digital_signature = data.get('digital_signature')
    

    prescription = Prescription.find_by_prescription_number(prescription_number)
    if not prescription:
        return jsonify({'message': 'prescription not found', 'is_valid': False}), 200

    message = f"{prescription.prescription_number}|{prescription.patient_name}|{prescription.patient_age}|{prescription.medicine}|{prescription.gender_choice}|{prescription.patient_weight}|{prescription.patient_allergies}".encode('utf-8')
    is_valid = DSGen.verify_signature(message, digital_signature)


    if is_valid:
        return jsonify({
            'message': 'prescription is valid',
            'is_valid': True,
            'prescription_details': {
                'name': prescription.patient_name,
                'age': prescription.patient_age,
                'gender': prescription.gender_choice,
                'weight': prescription.patient_weight,
                'allergies': prescription.patient_allergies,
                'medicines': prescription.medicine
            }
        }), 200
    else:
        return jsonify({'message': 'prescription is invalid', 'is_valid': False}), 200

if __name__ == '__main__':
    app.run(port=8000)