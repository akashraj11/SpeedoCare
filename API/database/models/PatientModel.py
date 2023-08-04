"""
Models for Patient
"""
class Patient:
    def __init__(self, patient_id, prescriptions, details, medical_history):
        self.patient_id = patient_id
        self.prescriptions = prescriptions
        self.details = details
        self.medical_history = medical_history
