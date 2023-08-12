from itsdangerous import URLSafeTimedSerializer
from flask import session, current_app

def generate_auth_token(user_id):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    auth_token = serializer.dumps({'user_id': user_id})
    return auth_token

def store_user_in_session(user_id):
    session['user_id'] = user_id

def clear_user_from_session():
    session.pop('user_id', None)
