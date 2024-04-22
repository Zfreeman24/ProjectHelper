import unittest
from backend.auth_controller import verify_login, register

class TestAuthController(unittest.TestCase):

    def test_verify_login_success(self):
        email = "test@example.com"
        password = "password123".encode('utf-8')
        response = verify_login(email, password)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Login successful', 'status': 'success'})
    
    def test_verify_login_invalid_credentials(self):
        email = "invalid@email.com"
        password = "wrongpassword".encode('utf-8')
        response = verify_login(email, password)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {'message': 'Invalid credentials or not verified', 'status': 'error'})

    def test_verify_login_not_verified(self):
        email = "notverified@email.com" 
        password = "validpassword".encode('utf-8')
        response = verify_login(email, password)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {'message': 'Invalid credentials or not verified', 'status': 'error'})

    def test_register_success(self):
        name = "John Doe"
        email = "john@doe.com"
        password = "newpassword".encode('utf-8')
        is_verified = True
        response = register(name, email, password, is_verified)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Registration successful.'})
    
    def test_register_duplicate_email(self):
        name = "Jane Doe"
        email = "john@doe.com" 
        password = "somepassword".encode('utf-8')
        is_verified = True
        response = register(name, email, password, is_verified)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'message': 'Email already exists'})

