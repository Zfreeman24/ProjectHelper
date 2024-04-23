from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import bcrypt
import os
import logging

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv('MONGO_CLIENT'))
db = client[os.getenv('CLIENT')]
login_collection = db['login_info']  # Assuming you use the same collection for both

# Configure logging
logging.basicConfig(level=logging.INFO)


@app.route('/login', methods=['POST'])
def verify_login():
    data = request.json
    email = data['email']
    user_submitted_password = data['password'].encode('utf-8')
    user = login_collection.find_one({'email': email})
    
    if user and bcrypt.checkpw(user_submitted_password, user['password']) and user['isVerified']:
        return jsonify({'message': 'Login successful', 'status': 'success'}), 200
    else:
        return jsonify({'message': 'Invalid credentials or not verified', 'status': 'error'}), 401


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']
    is_verified = data['isVerified']
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
    return jsonify({'message': 'Registration successful.'})


if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', False))
