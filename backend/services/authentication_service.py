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
    def verify_login(email, password):
        user = login_collection.find_one({'email': email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']) and user['isVerified']:
            return True, 'Login successful'
        else:
            return False, 'Invalid credentials or not verified'

    def register(name, email, password, is_verified):
        if isinstance(password, str):  # Check if the password is a string and convert if necessary
            password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        user_data = {
            'name': name,
            'email': email,
            'password': hashed_password,
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
    message = auth_service.register(data['name'], data['email'], data['password'], data['isVerified'])
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', False))