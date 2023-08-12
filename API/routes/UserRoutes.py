""" 
User routes
"""
from flask import request, jsonify
from API.database.models.UserModel import User
from API.common.helperFunction import create_user_object
from API.common.helperFunction import create_patient_object
from API.common.helperFunction import create_clinic_admin_object
from API.common.helperFunction import create_doctor_object
from API.common.helperFunction import create_patient_object_post
from API.common.helperFunction import create_clinic_admin_object_post
from API.common.helperFunction import create_doctor_object_post
from API.common.helperFunction import user_to_dict
from API.database.connection.config import get_connection
from flask import Blueprint

user_blueprint = Blueprint('user', __name__)

# Create a new user with nested objects
@user_blueprint.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Request data is missing"}), 400

        new_user = User(
            None,
            data["username"],
            data["first_name"],
            data["last_name"],
            data["contact_no"],
            data["email"],
            data["encrypted_password"],
            data["address"],
            data["date_of_birth"],
            data["user_role"],
        )

        patient_data = data.get("patient", {})
        clinic_admin_data = data.get("clinic_admin", {})
        doctor_data = data.get("doctor", {})

        if patient_data or clinic_admin_data or doctor_data:
            connection = get_connection()
            if connection is None:
                return jsonify({"message": "Error connecting to the database"}), 500

            cursor = connection.cursor()
            try:
                connection.start_transaction()

                cursor.execute(
                    "INSERT INTO users (username, first_name, last_name, contact_no, email, encrypted_password, address, date_of_birth, user_role) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        new_user.username,
                        new_user.first_name,
                        new_user.last_name,
                        new_user.contact_no,
                        new_user.email,
                        new_user.encrypted_password,
                        new_user.address,
                        new_user.date_of_birth,
                        new_user.user_role,
                    ),
                )

                new_user.user_id = cursor.lastrowid

                if patient_data:
                    patient = create_patient_object_post(None, patient_data)
                    cursor.execute(
                        "INSERT INTO patients (user_id, prescriptions, details, medical_history) "
                        "VALUES (%s, %s, %s, %s)",
                        (
                            new_user.user_id,
                            patient.prescriptions,
                            patient.details,
                            patient.medical_history,
                        ),
                    )
                    patient.patient_id = cursor.lastrowid
                    new_user.patient = patient

                if clinic_admin_data:
                    clinic_admin = create_clinic_admin_object_post(
                        None, clinic_admin_data
                    )
                    cursor.execute(
                        "INSERT INTO clinic_admins (user_id, clinic_internal_id, clinic_id) "
                        "VALUES (%s, %s, %s)",
                        (
                            new_user.user_id,
                            clinic_admin.clinic_internal_id,
                            clinic_admin.clinic_id,
                        ),
                    )
                    clinic_admin.clinic_admin_id = cursor.lastrowid
                    new_user.clinic_admin = clinic_admin

                if doctor_data:
                    doctor = create_doctor_object_post(None, doctor_data)
                    cursor.execute(
                        "INSERT INTO doctors (user_id, clinic_id, specialization) "
                        "VALUES (%s, %s, %s)",
                        (new_user.user_id, doctor.clinic_id, doctor.specialization),
                    )
                    doctor.doctor_id = cursor.lastrowid
                    new_user.doctor = doctor

                connection.commit()
                cursor.close()
                connection.close()

                return jsonify(user_to_dict(new_user)), 201
            except Exception as e:
                connection.rollback()
                print("Error:", e)
                return (
                    jsonify({"message": "Error creating the user with nested objects"}),
                    500,
                )

        else:
            return (
                jsonify(
                    {
                        "message": "At least one nested object (patient, clinic_admin, or doctor) is required"
                    }
                ),
                400,
            )
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error creating the user with nested objects"}), 500

# Get all users with nested objects
@user_blueprint.route("/users", methods=["GET"])
def get_all_user():
    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users_data = cursor.fetchall()
        users = []
        for user_data in users_data:
            user = create_user_object(user_data)

            cursor.execute("SELECT * FROM patients WHERE user_id=%s", (user.user_id,))
            patient_data = cursor.fetchone()
            if patient_data:
                patient = create_patient_object(patient_data)
                user.patient = patient

            cursor.execute(
                "SELECT * FROM clinic_admins WHERE user_id=%s", (user.user_id,)
            )
            clinic_admin_data = cursor.fetchone()
            if clinic_admin_data:
                clinic_admin = create_clinic_admin_object(clinic_admin_data)
                user.clinic_admin = clinic_admin

            cursor.execute("SELECT * FROM doctors WHERE user_id=%s", (user.user_id,))
            doctor_data = cursor.fetchone()
            if doctor_data:
                doctor = create_doctor_object(doctor_data)
                user.doctor = doctor

            users.append(user_to_dict(user))

        cursor.close()
        connection.close()

        return jsonify(users), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error fetching users"}), 500

# Get a user by ID with nested objects
@user_blueprint.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            user = create_user_object(user_data)

            cursor.execute("SELECT * FROM patients WHERE user_id=%s", (user_id,))
            patient_data = cursor.fetchone()
            if patient_data:
                patient = create_patient_object(patient_data)
                user.patient = patient

            cursor.execute("SELECT * FROM clinic_admins WHERE user_id=%s", (user_id,))
            clinic_admin_data = cursor.fetchone()
            if clinic_admin_data:
                clinic_admin = create_clinic_admin_object(clinic_admin_data)
                user.clinic_admin = clinic_admin

            cursor.execute("SELECT * FROM doctors WHERE user_id=%s", (user_id,))
            doctor_data = cursor.fetchone()
            if doctor_data:
                doctor = create_doctor_object(doctor_data)
                user.doctor = doctor

            cursor.close()
            connection.close()

            return jsonify(user_to_dict(user)), 200
        else:
            cursor.close()
            connection.close()
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error fetching the user"}), 500

# Delete a user by ID with nested objects
@user_blueprint.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))

            # Also delete the related nested objects if they exist
            cursor.execute("DELETE FROM patients WHERE user_id=%s", (user_id,))
            cursor.execute("DELETE FROM clinic_admins WHERE user_id=%s", (user_id,))
            cursor.execute("DELETE FROM doctors WHERE user_id=%s", (user_id,))

            connection.commit()
            cursor.close()
            connection.close()

            return (
                jsonify({"message": "User and nested objects deleted successfully"}),
                200,
            )
        else:
            cursor.close()
            connection.close()
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error deleting the user and nested objects"}), 500

# Delete all users and nested objects
@user_blueprint.route("/users/all", methods=["DELETE"])
def delete_all_users():
    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()

        # Delete all users
        cursor.execute("DELETE FROM users")

        # Also delete all related nested objects
        cursor.execute("DELETE FROM patients")
        cursor.execute("DELETE FROM clinic_admins")
        cursor.execute("DELETE FROM doctors")

        connection.commit()
        cursor.close()
        connection.close()

        return (
            jsonify({"message": "All users and nested objects deleted successfully"}),
            200,
        )

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error deleting all users and nested objects"}), 500

# Update a user by ID with nested objects
@user_blueprint.route("/users/<int:user_id>", methods=["PUT"])
def update_user_by_id(user_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Request data is missing"}), 400

        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()

        # Check if the user exists
        cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
        user_data = cursor.fetchone()
        if not user_data:
            cursor.close()
            connection.close()
            return jsonify({"message": "User not found"}), 404

        # Update user details
        cursor.execute(
            "UPDATE users SET username=%s, first_name=%s, last_name=%s, contact_no=%s, email=%s, encrypted_password=%s, address=%s, date_of_birth=%s, user_role=%s WHERE user_id=%s",
            (
                data["username"],
                data["first_name"],
                data["last_name"],
                data["contact_no"],
                data["email"],
                data["encrypted_password"],
                data["address"],
                data["date_of_birth"],
                data["user_role"],
                user_id,
            ),
        )

        # Check for nested object updates
        patient_data = data.get("patient", {})
        if patient_data:
            cursor.execute("SELECT * FROM patients WHERE user_id=%s", (user_id,))
            existing_patient_data = cursor.fetchone()
            if existing_patient_data:
                cursor.execute(
                    "UPDATE patients SET prescriptions=%s, details=%s, medical_history=%s WHERE user_id=%s",
                    (
                        patient_data["prescriptions"],
                        patient_data["details"],
                        patient_data["medical_history"],
                        user_id,
                    ),
                )
            else:
                cursor.execute(
                    "INSERT INTO patients (user_id, prescriptions, details, medical_history) "
                    "VALUES (%s, %s, %s, %s)",
                    (
                        user_id,
                        patient_data["prescriptions"],
                        patient_data["details"],
                        patient_data["medical_history"],
                    ),
                )

        clinic_admin_data = data.get("clinic_admin", {})
        if clinic_admin_data:
            cursor.execute("SELECT * FROM clinic_admins WHERE user_id=%s", (user_id,))
            existing_clinic_admin_data = cursor.fetchone()
            if existing_clinic_admin_data:
                cursor.execute(
                    "UPDATE clinic_admins SET clinic_internal_id=%s, clinic_id=%s WHERE user_id=%s",
                    (
                        clinic_admin_data["clinic_internal_id"],
                        clinic_admin_data["clinic_id"],
                        user_id,
                    ),
                )
            else:
                cursor.execute(
                    "INSERT INTO clinic_admins (user_id, clinic_internal_id, clinic_id) "
                    "VALUES (%s, %s, %s)",
                    (
                        user_id,
                        clinic_admin_data["clinic_internal_id"],
                        clinic_admin_data["clinic_id"],
                    ),
                )

        doctor_data = data.get("doctor", {})
        if doctor_data:
            cursor.execute("SELECT * FROM doctors WHERE user_id=%s", (user_id,))
            existing_doctor_data = cursor.fetchone()
            if existing_doctor_data:
                cursor.execute(
                    "UPDATE doctors SET clinic_id=%s, specialization=%s WHERE user_id=%s",
                    (doctor_data["clinic_id"], doctor_data["specialization"], user_id),
                )
            else:
                cursor.execute(
                    "INSERT INTO doctors (user_id, clinic_id, specialization) "
                    "VALUES (%s, %s, %s)",
                    (user_id, doctor_data["clinic_id"], doctor_data["specialization"]),
                )

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error updating the user with nested objects"}), 500

# Search users by first name, last name, or user role
@user_blueprint.route("/users/search", methods=["GET"])
def search_users():
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    user_role = request.args.get("user_role")

    # Replace this function with the logic to search users in the database based on the provided parameters
    # For example, execute a SELECT query on the users table with appropriate WHERE conditions
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE 1"
    parameters = []

    if first_name:
        query += " AND first_name LIKE %s"
        parameters.append(f"%{first_name}%")

    if last_name:
        query += " AND last_name LIKE %s"
        parameters.append(f"%{last_name}%")

    if user_role:
        query += " AND user_role = %s"
        parameters.append(user_role)

    cursor.execute(query, tuple(parameters))
    users_data = cursor.fetchall()
    cursor.close()
    connection.close()

    # Convert the fetched data to a list of dictionaries
    users_list = [user_to_dict(User(*data)) for data in users_data]

    return jsonify(users_list), 200

# Get all users with nested objects
@user_blueprint.route("/users/doctors/specialization/<string:specialization>", methods=["GET"])
def get_all_doctors_by_specialization(specialization):
    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users where user_role='Doctor'")
        users_data = cursor.fetchall()
        users = []
        for user_data in users_data:
            user = create_user_object(user_data)

            cursor.execute("SELECT * FROM doctors WHERE user_id=%s and specialization=%s", (user.user_id,specialization))
            doctor_data = cursor.fetchone()
            if doctor_data:
                doctor = create_doctor_object(doctor_data)
                user.doctor = doctor
                users.append(user_to_dict(user))

        cursor.close()
        connection.close()

        return jsonify(users), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error fetching users"}), 500

# Get all users with nested objects
@user_blueprint.route("/users/doctors/clinic/<string:clinic_id>", methods=["GET"])
def get_all_doctors_by_clinic(clinic_id):
    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users where user_role='Doctor'")
        users_data = cursor.fetchall()
        users = []
        for user_data in users_data:
            user = create_user_object(user_data)

            cursor.execute("SELECT * FROM doctors WHERE user_id=%s and clinic_id=%s", (user.user_id,clinic_id))
            doctor_data = cursor.fetchone()
            if doctor_data:
                doctor = create_doctor_object(doctor_data)
                user.doctor = doctor
                users.append(user_to_dict(user))

        cursor.close()
        connection.close()

        return jsonify(users), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error fetching users"}), 500
