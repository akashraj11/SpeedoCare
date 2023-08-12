from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from API.routes.UserRoutes import user_blueprint
from API.routes.LoginRoute import login_blueprint
from API.routes.notificationRoutes import notification_blueprint
from API.routes.ClinicRoute import clinic_blueprint
from API.routes.AppointmentRoute import appointment_blueprint
from API.routes.ReviewRoute import review_blueprint
from API.database.models.UserModel import User
from API.database.connection.config import get_connection

# Define root path as /speedocare/
app = Flask(__name__, root_path="/speedocare")
app.debug = True  # Turn on debug mode
app.secret_key = 'speedocare_secret_key'
app.register_blueprint(user_blueprint, url_prefix='/speedocare')
app.register_blueprint(login_blueprint, url_prefix='/speedocare')
app.register_blueprint(notification_blueprint, url_prefix='/speedocare')
app.register_blueprint(clinic_blueprint, url_prefix='/speedocare')
app.register_blueprint(appointment_blueprint, url_prefix='/speedocare')
app.register_blueprint(review_blueprint, url_prefix='/speedocare')


CORS(app)
# Login manager
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    # Replace this function with the logic to load a user from the database
    # For example, execute a SELECT query on the users table using user_id
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    if row:
        return User(*row)
    else:
        return None


if __name__ == "__main__":
    # Local test
    app.run()

    # Prod
    # app.run(host='0.0.0.0', port=5050)
