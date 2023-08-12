from flask import request, jsonify
from API.database.models.ClinicModel import Clinic
from flask import Blueprint

clinic_blueprint = Blueprint('clinic', __name__)

# GET All Clinics
@clinic_blueprint.route("/clinics", methods=["GET"])
def get_all_clinics():
    clinics = Clinic.get_all_clinics()
    return jsonify([clinic.to_dict() for clinic in clinics]), 200

# GET Clinic by ID
@clinic_blueprint.route("/clinics/<int:clinic_id>", methods=["GET"])
def get_clinic_by_id(clinic_id):
    clinic = Clinic.get_clinic_by_id(clinic_id)
    if clinic:
        return jsonify(clinic.to_dict()), 200
    else:
        return jsonify({"message": "Clinic not found"}), 404

# POST Create a New Clinic
@clinic_blueprint.route("/clinics", methods=["POST"])
def create_clinic():
    data = request.get_json()
    clinic = Clinic(None, data.get("location"), data.get("clinic_name"), data.get("description"))
    clinic.save()
    return jsonify({"message": "Clinic created successfully"}), 201

# PUT Update Clinic by ID
@clinic_blueprint.route("/clinics/<int:clinic_id>", methods=["PUT"])
def update_clinic_by_id(clinic_id):
    data = request.get_json()
    clinic = Clinic.get_clinic_by_id(clinic_id)
    if clinic:
        clinic.location = data.get("location")
        clinic.clinic_name = data.get("clinic_name")
        clinic.description = data.get("description")
        clinic.update()
        return jsonify({"message": "Clinic updated successfully"}), 200
    else:
        return jsonify({"message": "Clinic not found"}), 404

# DELETE Clinic by ID
@clinic_blueprint.route("/clinics/<int:clinic_id>", methods=["DELETE"])
def delete_clinic_by_id(clinic_id):
    clinic = Clinic.get_clinic_by_id(clinic_id)
    if clinic:
        clinic.delete()
        return jsonify({"message": "Clinic deleted successfully"}), 200
    else:
        return jsonify({"message": "Clinic not found"}), 404

# GET Clinic by Name
@clinic_blueprint.route("/clinics/<string:clinic_name>", methods=["GET"])
def get_clinic_by_name(clinic_name):
    clinics = Clinic.get_clinic_by_Name(clinic_name)  # Modify this method to return a list of clinics
    if clinics:
        clinic_list = [clinic.to_dict() for clinic in clinics]
        return jsonify(clinic_list), 200
    else:
        return jsonify({"message": "Clinics not found"}), 404