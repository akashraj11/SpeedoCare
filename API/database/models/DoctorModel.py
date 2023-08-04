"""
Models for Doctor
"""
class Doctor:
    def __init__(self, doctor_id, clinic_id, specialization):
        self.doctor_id = doctor_id
        self.clinic_id = clinic_id
        self.specialization = specialization