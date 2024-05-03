from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import bcrypt
import os
import logging
from ..interfaces.auth_interface import AuthInterface

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv('MONGO_CLIENT'))
db = client[os.getenv('CLIENT')]
login_collection = db['login_info']

logging.basicConfig(level=logging.INFO)

class AuthenticationService(AuthInterface):
   def verify_login(self, email, password):
        user = login_collection.find_one({'email': email})
        if user:
            # Check if 'isVerified' key exists, default to False if not present
            is_verified = user.get('isVerified', False)
            if password == user['password'] and is_verified:
                return True, 'Login successful'
        return False, 'Invalid credentials or not verified'

   def register(self, name, email, password, is_verified):  # `self` comes first in the argument list
        if isinstance(password, str):  # Ensure password is a byte string
            password = password.encode('utf-8')
        user_data = {
            'name': name,
            'email': email,
            'password': password,
            'isVerified': is_verified
        }
        login_collection.insert_one(user_data)
        logging.info("Registration successful")
        return 'Registration successful.'

auth_service = AuthenticationService()

@app.route('/login', methods=['POST'])
def login_route():
    data = request.json
    success, message = auth_service.verify_login(data['email'], data['password'])
    if success:
        return jsonify({'message': message, 'status': 'success'}), 200
    else:
        return jsonify({'message': message, 'status': 'error'}), 401

@app.route('/register', methods=['POST'])
def register_route():
    data = request.json
    password = data['password']
    print(password)
    name = data['name']
    email = data['email']
    is_verified = data['isVerified']
    message = auth_service.register(name, email, password, is_verified)
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(host = "localhost", debug=os.getenv('FLASK_DEBUG', False))