import json
import pytest
from flask import Flask
from API.routes.ClinicRoutes import clinic_blueprint

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(clinic_blueprint)
    client = app.test_client()
    return client

def test_get_all_clinics(client):
    response = client.get("/clinics")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_get_clinic_by_id(client):
    response = client.get("/clinics/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)

def test_get_clinic_by_invalid_id(client):
    response = client.get("/clinics/999")
    assert response.status_code == 404

# Similar tests for other endpoints: create_clinic, update_clinic_by_id, delete_clinic_by_id, get_clinic_by_name
# ...

if __name__ == "__main__":
    pytest.main()
