"""
Models for Appointment
"""
class Appointment:
    def __init__(self, appointment_id, patient_id, doctor_id, clinic_id, booking_date, booking_information, comment, price, status, follow_up_req):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.clinic_id = clinic_id
        self.booking_date = booking_date
        self.booking_information = booking_information
        self.comment = comment
        self.price = price
        self.status = status
        self.follow_up_req = follow_up_req
