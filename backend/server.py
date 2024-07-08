from flask import Flask, request, jsonify
import random
from models.prescription import Prescription
from utils.digital_signature import DigitalSignature

# Constants
PRIVATE_KEY_FILE = 'keys/private.pem'
PUBLIC_KEY_FILE = 'keys/public.pem'
DIGITAL_SIGNATURE_SEPARATOR = '|'
PRESCRIPTION_NUMBER_LENGTH = 10
SUCCESS_STATUS_CODE = 200

# Load keys
private_key = open(PRIVATE_KEY_FILE).read()
public_key = open(PUBLIC_KEY_FILE).read()

# Initialize digital signature generator
DSGen = DigitalSignature(private_key, public_key)

app = Flask(__name__)

def generate_prescription_number():
    """Generate a random prescription number of fixed length."""
    return ''.join([str(random.randint(0, 9)) for _ in range(PRESCRIPTION_NUMBER_LENGTH)])

def serialize_prescription(prescription):
    """Serialize prescription details for digital signature."""
    medicines_str = DIGITAL_SIGNATURE_SEPARATOR.join(
        [f"{med['name']}:{med['dosage']}:{med['frequency']}" for med in prescription['medicines']])
    return DIGITAL_SIGNATURE_SEPARATOR.join([
        prescription['prescription_number'],
        prescription['patient_name'],
        str(prescription['patient_age']),
        medicines_str,
        prescription['gender_choice'],
        str(prescription['patient_weight']),
        prescription['patient_allergies']
    ]).encode('utf-8')

@app.route('/issue-prescription', methods=['POST'])
def issue_prescription():
    """Issue a new prescription."""
    data = request.get_json()
    prescription = {
        'prescription_number': generate_prescription_number(),
        'patient_name': data.get('name'),
        'patient_age': data.get('age'),
        'medicines': data.get('medicines', []),
        'gender_choice': data.get('gender'),
        'patient_weight': data.get('weight'),
        'patient_allergies': data.get('allergies')
    }

    digital_signature_str = DSGen.generate_signature(serialize_prescription(prescription))

    prescription_obj = Prescription(**prescription, digital_signature=digital_signature_str)
    prescription_obj.save()

    return jsonify({'message': 'prescription issued successfully', 'prescription_number': prescription['prescription_number'], 'digital_signature': digital_signature_str}), SUCCESS_STATUS_CODE

@app.route('/verify-prescription', methods=['POST'])
def verify_prescription():
    """Verify an existing prescription."""
    data = request.get_json()
    prescription_number = data.get('prescription_number')
    digital_signature = data.get('digital_signature')

    prescription = Prescription.find_by_prescription_number(prescription_number)
    if not prescription:
        return jsonify({'message': 'prescription not found', 'is_valid': False}), SUCCESS_STATUS_CODE

    is_valid = DSGen.verify_signature(serialize_prescription(prescription.__dict__), digital_signature)

    if is_valid:
        return jsonify({
            'message': 'prescription is valid',
            'is_valid': True,
            'prescription_details': prescription.__dict__
        }), SUCCESS_STATUS_CODE
    else:
        return jsonify({'message': 'prescription is invalid', 'is_valid': False}), SUCCESS_STATUS_CODE

if __name__ == '__main__':
    app.run(port=8000)