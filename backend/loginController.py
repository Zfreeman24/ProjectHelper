from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import uuid
import sendEmail

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb+srv://zacharyjames888:utsa5150@cluster0.13apwst.mongodb.net/')  
db = client['project_helper'] 

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']
    
    isVerified = False;
    
    print("success")
    user_data = {
        'name': name,
        'email': email,
        'password': password,
        'isVerified': isVerified
    }
    
    collection = db["login_info"]
    collection.insert_one(user_data)
    
    verification_token = ''
    sendEmail.send_verification_email(email, verification_token)
    
    
    return jsonify({'message': 'Registration successful. Verification email sent.'})
    


if __name__ == '__main__':
    app.run(debug=True)
