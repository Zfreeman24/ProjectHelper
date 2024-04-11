from flask import Flask, request
import bcrypt
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import logging
import os

load_dotenv()

client = MongoClient(os.getenv('MONGO_CLIENT'))  
db = client[os.getenv('CLIENT')]
collection = db[os.getenv('COLLECTION')] 
app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def verifyLogin():
    logging.info("Grabbing data")
    data = request.json
    email = data['email']
    user_submitted_password = data['password'].encode('utf-8')  # Encode the password into bytes

    user = collection.find_one({'email': email})
    if user:
        stored_hashed_password = user['password']  # Assuming this is already in bytes from MongoDB
        isVerified = user['isVerified']
    
        # Verifying the password
        if bcrypt.checkpw(user_submitted_password, stored_hashed_password) and isVerified:
            logging.info("Login success")
            return "Login successful", 200
        else:
            logging.info("Login failed")
            return "Invalid credentials or not verified", 401
    else:
        logging.info("No user found with that email")
        return "User not found", 404

if __name__ == '__main__':
    app.run(debug=True)
