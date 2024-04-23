import unittest
from unittest.mock import patch

from backend.auth_controller import app, verify_login, register

class AuthControllerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_verify_login_success(self):
        test_user = {'email': 'test@example.com', 'password': 'password123'}
        response = self.app.post('/login', json=test_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Login successful', 'status': 'success'})
    
    def test_verify_login_invalid_credentials(self):
        test_user = {'email': 'invalid@example.com', 'password': 'invalidpass'}
        response = self.app.post('/login', json=test_user)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {'message': 'Invalid credentials or not verified', 'status': 'error'})

    @patch('backend.auth_controller.bcrypt')
    def test_register(self, mock_bcrypt):
        test_user = {'name': 'Test User', 'email': 'test@example.com', 'password': 'password123', 'isVerified': True}
        mock_bcrypt.gensalt.return_value = b'salt'
        mock_bcrypt.hashpw.return_value = b'hashedpassword'
        response = self.app.post('/register', json=test_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Registration successful.'})

