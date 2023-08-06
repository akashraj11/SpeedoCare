from flask import request, jsonify

from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user,
)
from API.database.connection.config import get_connection
from API.database.models.UserModel import User
from flask import Blueprint
from flask import request, jsonify
from flask_login import login_user, login_required, logout_user, current_user

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Replace this function with the logic to fetch the user from the database using the username
    # For example, execute a SELECT query on the users table using the username
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    if row and password == row[6]:  # Assuming the password is stored in the 7th column of the users table
        user = User(*row)
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@login_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200


@login_blueprint.route('/profile', methods=['GET'])
@login_required
def profile():
    return jsonify({
        "user_id": current_user.user_id,
        "username": current_user.username,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "contact_no": current_user.contact_no,
        "email": current_user.email,
        "address": current_user.address,
        "date_of_birth": current_user.date_of_birth,
        "user_role": current_user.user_role
    }), 200
