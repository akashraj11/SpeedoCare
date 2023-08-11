"""
Models for Review
"""
class Review:
    def __init__(self, review_id, patient_id, doctor_id, clinic_id, rating, review_text, reported, reviewed_for):
        self.review_id = review_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.clinic_id = clinic_id
        self.rating = rating
        self.review_text = review_text
        self.reported = reported
        self.reviewed_for = reviewed_for
