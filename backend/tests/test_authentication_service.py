import unittest
from unittest.mock import patch

from authentication_service import AuthenticationService

class TestAuthenticationService(unittest.TestCase):

    def setUp(self):
        self.auth_service = AuthenticationService()

    def test_verify_login_success(self):
        email = 'test@example.com'
        password = 'password123'
        with patch('authentication_service.login_collection') as mock_collection:
            mock_user = {'email': email, 'password': b'$2b$12$C1b2B7k8cN0c9d3e4f5g6h7i8j9k0l1', 'isVerified': True}
            mock_collection.find_one.return_value = mock_user
            success, message = self.auth_service.verify_login(email, password)
        
        self.assertTrue(success)
        self.assertEqual(message, 'Login successful')

    def test_verify_login_wrong_password(self):
        email = 'test@example.com'
        password = 'wrongpassword'
        with patch('authentication_service.login_collection') as mock_collection:
            mock_user = {'email': email, 'password': b'$2b$12$C1b2B7k8cN0c9d3e4f5g6h7i8j9k0l1', 'isVerified': True}
            mock_collection.find_one.return_value = mock_user
            success, message = self.auth_service.verify_login(email, password)
        
        self.assertFalse(success)
        self.assertEqual(message, 'Invalid credentials or not verified')

    def test_verify_login_not_verified(self):
        email = 'test@example.com'
        password = 'password123'
        with patch('authentication_service.login_collection') as mock_collection:
            mock_user = {'email': email, 'password': b'$2b$12$C1b2B7k8cN0c9d3e4f5g6h7i8j9k0l1', 'isVerified': False}
            mock_collection.find_one.return_value = mock_user
            success, message = self.auth_service.verify_login(email, password)
        
        self.assertFalse(success)
        self.assertEqual(message, 'Invalid credentials or not verified')

    def test_verify_login_user_not_found(self):
        email = 'test@example.com'
        password = 'password123'
        with patch('authentication_service.login_collection') as mock_collection:
            mock_collection.find_one.return_value = None
            success, message = self.auth_service.verify_login(email, password)
        
        self.assertFalse(success)
        self.assertEqual(message, 'Invalid credentials or not verified')

