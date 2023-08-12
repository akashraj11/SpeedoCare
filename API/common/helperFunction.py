""" 
Helper function
"""
from API.database.models.ClinicAdminModel import ClinicAdmin
from API.database.models.UserModel import User
from API.database.models.DoctorModel import Doctor
from API.database.models.PatientModel import Patient


# Helper functions for converting model objects to dictionaries and vice versa
def create_user_object(data):
    return User(
        data[0],
        data[1],
        data[2],
        data[3],
        data[4],
        data[5],
        data[6],
        data[7],
        data[8],
        data[9],
    )

def create_patient_object(data):
    return Patient(data[0], data[2], data[3], data[4])


def create_clinic_admin_object(data):
    return ClinicAdmin(data[0], data[2], data[3])


def create_doctor_object(data):
    return Doctor(data[0], data[2], data[3])


# For Post Using dict
def create_patient_object_post(patient_id, data):
    return Patient(
        patient_id, data["prescriptions"], data["details"], data["medical_history"]
    )


def create_clinic_admin_object_post(clinic_admin_id, data):
    return ClinicAdmin(clinic_admin_id, data["clinic_internal_id"], data["clinic_id"])


def create_doctor_object_post(doctor_id, data):
    return Doctor(doctor_id, data["clinic_id"], data["specialization"])


def user_to_dict(user):
    user_dict = {
        "user_id": user.user_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "contact_no": user.contact_no,
        "email": user.email,
        "encrypted_password": user.encrypted_password,
        "address": user.address,
        "date_of_birth": user.date_of_birth,
        "user_role": user.user_role,
    }
    if user.patient:
        user_dict["patient"] = {
            "patient_id": user.patient.patient_id,
            "prescriptions": user.patient.prescriptions,
            "details": user.patient.details,
            "medical_history": user.patient.medical_history,
        }
    if user.clinic_admin:
        user_dict["clinic_admin"] = {
            "clinic_admin_id": user.clinic_admin.clinic_admin_id,
            "clinic_internal_id": user.clinic_admin.clinic_internal_id,
            "clinic_id": user.clinic_admin.clinic_id,
        }
    if user.doctor:
        user_dict["doctor"] = {
            "doctor_id": user.doctor.doctor_id,
            "clinic_id": user.doctor.clinic_id,
            "specialization": user.doctor.specialization,
        }
    return user_dict


