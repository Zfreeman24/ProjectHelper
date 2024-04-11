from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv('MONGO_CLIENT'))  
db = client[os.getenv('CLIENT')] 

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']
    isVerified = data['isVerified']
    
    #bcrypt the password
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)

    print("success")
    user_data = {
        'name': name,
        'email': email,
        'password': hashed_password,
        'isVerified': isVerified
    }
    
    collection = db["login_info"]
    collection.insert_one(user_data)
    
    return jsonify({'message': 'Registration successful.'})

if __name__ == '__main__':
    app.run(debug=True)
