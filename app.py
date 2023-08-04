from flask import Flask
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from API.routes.UserRoutes import api_blueprint

# Define root path as /speedocare/
app = Flask(__name__, root_path="/speedocare")
app.debug = True  # Turn on debug mode
app.register_blueprint(api_blueprint, url_prefix='/speedocare')

CORS(app)


if __name__ == "__main__":
    app.run()
