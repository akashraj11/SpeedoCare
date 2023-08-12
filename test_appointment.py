import pytest
import json
from flask import app
#from flask import Flask
#from Speedocare.SpeedoCare.app import app
from API.database.connection.config import get_connection

BASE_URL = "http://127.0.0.1:5000/speedocare"


@pytest.fixture
def client():
    app.config["TESTING"] = True  # Set the app in testing mode
    with app.test_client() as test_client:
        yield test_client
# Test GET /appointments
def test_get_appointments(client):
    response = client.get(f"{BASE_URL}/appointments")
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert isinstance(data, list)

# Test POST /appointments
def test_create_appointment(client):
    new_appointment = {
        "appointment_id": 1,
        "patient_id": 1,
        "doctor_id": 1,
        "clinic_id": 1,
        "booking_date": "2023-08-05",
        "booking_information": "Some information",
        "comment": "Some comment",
        "price": 100.00,
        "status": "Pending",
        "follow_up_req": "Follow up required"
    }
    response = client.post(f"{BASE_URL}/appointments", json=new_appointment)
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 201
    assert "message" in data and data["message"] == "Appointment created successfully."

# Test GET /appointments/<appointment_id>
def test_get_appointment_by_id(client):
    appointment_id = 1
    response = client.get(f"{BASE_URL}/appointments/{appointment_id}")
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert "appointment_id" in data and data["appointment_id"] == appointment_id

