import pytest
from flask import Flask
from API.routes.notification_routes import notification_blueprint

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(notification_blueprint)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_notification(client):
    response = client.post('/notifications', json={
        "notification_date": "2023-08-05",
        "user_id": 1,
        "from_": "sender@example.com",
        "to_": "receiver@example.com",
        "cc": "cc@example.com",
        "bcc": "bcc@example.com",
        "subject": "Test Subject",
        "body": "Test Body",
        "digital_image": "image.png"
    })
    assert response.status_code == 201
    assert response.json == {"message": "Notification created successfully"}

def test_get_notifications(client):
    response = client.get('/notifications')
    assert response.status_code == 200
    # You can also assert the response JSON content here

# Add more test cases for other routes similarly

if __name__ == '__main__':
    pytest.main()
