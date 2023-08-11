""" 
NotificationS routes
"""
from flask import request, jsonify
from API.database.models.ReviewModel import Review
from API.database.connection.config import get_connection
from flask import Blueprint

review_blueprint = Blueprint('notifications', __name__)

# Create a new review
@review_blueprint.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    review = Review(
        data['review_id'],
        data['patient_id'],
        data['doctor_id'],
        data['clinic_id'],
        data['rating'],
        data['review_text'],
        data['reported'],
        data['reviewed_for']
    )
    reviews_data.append(review)
    return jsonify({"message": "Review created successfully."})

# Get all reviews
@review_blueprint('/reviews', methods=['GET'])
def get_reviews():
    return jsonify([{
        "review_id": r.review_id,
        "patient_id": r.patient_id,
        "doctor_id": r.doctor_id,
        "clinic_id": r.clinic_id,
        "rating": r.rating,
        "review_text": r.review_text,
        "reported": r.reported,
        "reviewed_for": r.reviewed_for
    } for r in reviews_data])

# Get a specific review by review_id
@review_blueprint('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = next((r for r in reviews_data if r.review_id == review_id), None)
    if review:
        return jsonify({
            "review_id": review.review_id,
            "patient_id": review.patient_id,
            "doctor_id": review.doctor_id,
            "clinic_id": review.clinic_id,
            "rating": review.rating,
            "review_text": review.review_text,
            "reported": review.reported,
            "reviewed_for": review.reviewed_for
        })
    else:
        return jsonify({"message": "Review not found."}), 404

# Get reviews by clinic_id
@review_blueprint('/reviews/clinic/<int:clinic_id>', methods=['GET'])
def get_reviews_by_clinic(clinic_id):
    clinic_reviews = [r for r in reviews_data if r.clinic_id == clinic_id]
    if clinic_reviews:
        return jsonify([{
            "review_id": r.review_id,
            "patient_id": r.patient_id,
            "doctor_id": r.doctor_id,
            "clinic_id": r.clinic_id,
            "rating": r.rating,
            "review_text": r.review_text,
            "reported": r.reported,
            "reviewed_for": r.reviewed_for
        } for r in clinic_reviews])
    else:
        return jsonify({"message": "No reviews found for the specified clinic ID."}), 404
