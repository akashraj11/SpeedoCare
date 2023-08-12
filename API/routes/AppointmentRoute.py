""" 
Appointment routes
"""
from flask import request, jsonify
from API.database.models.AppointmentModel import Appointment
from API.database.connection.config import get_connection
from flask import Blueprint

appointment_blueprint = Blueprint('api', __name__)

# Fetch all appointments
@appointment_blueprint.route("/appointments", methods=["GET"])
def get_appointments():
    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()

        query = "SELECT * FROM appointments"
        cursor.execute(query)
        result = cursor.fetchall()

        appointments_data = []
        for row in result:
            appointment = {
                "appointment_id": row[0],
                "patient_id": row[1],
                "doctor_id": row[2],
                "clinic_id": row[3],
                "booking_date": row[4],
                "booking_information": row[5],
                "comment": row[6],
                "price": row[7],
                "status": row[8],
                "follow_up_req": row[9],
                 }
            appointments_data.append(appointment)

        cursor.close()
        connection.close()

        return jsonify(appointments_data), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error retrieving appointments"}), 500    

# Create a new appointment
@appointment_blueprint.route('/appointments', methods=['POST'])
def create_appointment():
    try:
        data = request.get_json()

        appointment = Appointment(
            data['appointment_id'],
            data['patient_id'],
            data['doctor_id'],
            data['clinic_id'],
            data['booking_date'],
            data['booking_information'],
            data['comment'],
            data['price'],
            data['status'],
            data['follow_up_req'],
        )

        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()

        query = "INSERT INTO appointments (appointment_id, patient_id, doctor_id, clinic_id, booking_date, booking_information, comment, price, status, follow_up_req) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            appointment.appointment_id,
            appointment.patient_id,
            appointment.doctor_id,
            appointment.clinic_id,
            appointment.booking_date,
            appointment.booking_information,
            appointment.comment,
            appointment.price,
            appointment.status,
            appointment.follow_up_req,
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Appointment created successfully."}), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error creating the appointment"}), 500

# Get a specific appointment by appointment_id
@appointment_blueprint.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()

        query = "SELECT * FROM appointments WHERE appointment_id = %s"
        cursor.execute(query, (appointment_id,))
        result = cursor.fetchone()

        if result:
            appointment = Appointment(
                result[0],    # appointment_id
                result[1],    # patient_id
                result[2],    # doctor_id
                result[3],    # clinic_id
                result[4],    # booking_date
                result[5],    # booking_information
                result[6],    # comment
                result[7],    # price
                result[8],    # status
                result[9],    # follow_up_req
            )
            cursor.close()
            connection.close()

            return jsonify({
                "appointment_id": appointment.appointment_id,
                "patient_id": appointment.patient_id,
                "doctor_id": appointment.doctor_id,
                "clinic_id": appointment.clinic_id,
                "booking_date": appointment.booking_date,
                "booking_information": appointment.booking_information,
                "comment": appointment.comment,
                "price": appointment.price,
                "status": appointment.status,
                "follow_up_req": appointment.follow_up_req,
            }), 200
        else:
            cursor.close()
            connection.close()
            return jsonify({"message": "Appointment not found."}), 404

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error retrieving the appointment"}), 500

# Update an appointment by appointment_id
@appointment_blueprint.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    try:
        data = request.get_json()

        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()

        query = "UPDATE appointments SET patient_id = %s, doctor_id = %s, clinic_id = %s, booking_date = %s, booking_information = %s, comment = %s, price = %s, status = %s, follow_up_req = %s WHERE appointment_id = %s"
        values = (
            data['patient_id'],
            data['doctor_id'],
            data['clinic_id'],
            data['booking_date'],
            data['booking_information'],
            data['comment'],
            data['price'],
            data['status'],
            data['follow_up_req'],
            appointment_id,
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Appointment updated successfully."}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error updating the appointment"}), 500


# Get appointments by patient ID
@appointment_blueprint.route('/appointments/patient/<int:patient_id>', methods=['GET'])
def get_appointments_by_patient(patient_id):
    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()

        query = "SELECT * FROM appointments WHERE patient_id = %s"
        cursor.execute(query, (patient_id,))
        result = cursor.fetchall()

        appointments_data = []
        for row in result:
            appointment = {
                "appointment_id": row[0],
                "patient_id": row[1],
                "doctor_id": row[2],
                "clinic_id": row[3],
                "booking_date": row[4],
                "booking_information": row[5],
                "comment": row[6],
                "price": row[7],
                "status": row[8],
                "follow_up_req": row[9],
            }
            appointments_data.append(appointment)

        cursor.close()
        connection.close()

        return jsonify(appointments_data), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error retrieving appointments"}), 500
    
# Delete an appointment by appointment_id
@appointment_blueprint.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()

        query = "DELETE FROM appointments WHERE appointment_id = %s"
        cursor.execute(query, (appointment_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Appointment deleted successfully."}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error deleting the appointment"}), 500
