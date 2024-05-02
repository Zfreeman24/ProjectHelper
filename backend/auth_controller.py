from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user
import bcrypt
import os
import logging
import secrets
from ..interfaces.auth_interface import AuthInterface

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = secrets.token_hex(16)

client = MongoClient(os.getenv('MONGO_CLIENT'))
db = client[os.getenv('CLIENT')]
login_collection = db['login_info']

login_manager = LoginManager()
login_manager.init_app(app)

logging.basicConfig(level=logging.INFO)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

class AuthenticationService(AuthInterface):
    def verify_login(email, password):
        user = login_collection.find_one({'email': email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']) and user['isVerified']:
            user_obj = User(user['_id'])  
            login_user(user_obj)  
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

@app.route('/check_auth')
def check_auth():
    if current_user.is_authenticated:
        return jsonify({'authenticated': True, 'user_id': current_user.id})
    else:
        return jsonify({'authenticated': False})
    
@app.route('/logout')
@login_required
def logout():
    logout_user()  
    return jsonify({'message': 'Logged out successfully'})

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', False))