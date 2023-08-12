""" 
DB config
"""
from flask import Flask
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
'''
db_config = {
     'host': 'localhost',
     'port': 3306,
     'user': 'root',
     'password': 'Rahul',
     'database': 'speedocare'
 }
'''
db_config = {
    'host': 'speedocare.mysql.pythonanywhere-services.com',
    'port': 3306,
    'user': 'speedocare',
    'password': 'mysqlpass123',
    'database': 'speedocare$speedocare'
}

# Helper function to create a MySQL connection
def get_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print("Error while connecting to MySQL:", e)
        return None