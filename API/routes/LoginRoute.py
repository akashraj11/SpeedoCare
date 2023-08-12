from flask import app, request, jsonify

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
from API.database.connection.token_utils import generate_auth_token, store_user_in_session
from flask import session

login_blueprint = Blueprint('login', __name__)



# ...

@login_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    if row and password == row[6]:
        user = User(*row)

        # Generate a token containing user ID
        auth_token = generate_auth_token(user.user_id)

        # Store user information in the session
        store_user_in_session(user.user_id)

        return jsonify({"auth_token": auth_token, "user_id": user.user_id}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@login_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear
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
