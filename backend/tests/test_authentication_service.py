import unittest
from unittest.mock import patch, MagicMock

from backend.services.authentication_service import AuthenticationService

class TestAuthenticationService(unittest.TestCase):

    @patch('backend.services.authentication_service.login_collection')
    @patch('bcrypt.checkpw', return_value=True)
    def test_verify_login_success(self, mock_checkpw, mock_collection):
        mock_collection.find_one.return_value = {
            'email': 'test@example.com', 
            'password': b'$2b$12$C1jlVZo9gL4g9Yb3ZB.pSOOQphKJd9/ynl3tWJYW7ETsNOy1gah0O', 
            'isVerified': True
        }
        result = AuthenticationService.verify_login('test@example.com', 'password')
        self.assertTrue(result[0])
        self.assertEqual(result[1], 'Login successful')

    def test_verify_login_invalid_credentials(self):
        with patch('backend.services.authentication_service.login_collection.find_one', return_value=None):
            result = AuthenticationService.verify_login('invalid@email.com', 'wrongpassword')
            self.assertFalse(result[0])
            self.assertEqual(result[1], 'Invalid credentials or not verified')

    @patch('backend.services.authentication_service.login_collection')
    def test_verify_login_not_verified(self, mock_collection):
        mock_collection.find_one.return_value = {
            'email': 'test@example.com', 
            'password': b'$2b$12$C1jlVZo9gL4g9Yb3ZB.pSOOQphKJd9/ynl3tWJYW7ETsNOy1gah0O', 
            'isVerified': False
        }
        result = AuthenticationService.verify_login('test@example.com', 'password')
        self.assertFalse(result[0])
        self.assertEqual(result[1], 'Invalid credentials or not verified')

    def test_register_success(self):
        with patch('backend.services.authentication_service.login_collection.insert_one') as mock_insert:
            result = AuthenticationService.register('Test User', 'test@example.com', 'password123', True)
            self.assertEqual(result, 'Registration successful.')
            mock_insert.assert_called_once()
