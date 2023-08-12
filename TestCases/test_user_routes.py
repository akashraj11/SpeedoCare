import pytest
from flask import Flask
from API import app  # Import your Flask app instance
import json

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_create_user(client):
    # Test creating a user with nested objects
    data = {
        # Provide the necessary data for creating a user
    }
    response = client.post("/users", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    # Add assertions to validate the response data

def test_get_all_users(client):
    # Test getting all users with nested objects
    response = client.get("/users")
    assert response.status_code == 200
    # Add assertions to validate the response data

# Add more test functions for other routes
