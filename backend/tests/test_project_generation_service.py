import unittest
from unittest.mock import patch, call
import requests

from backend.services.project_generation_service import ProjectGenerationService

class TestProjectGenerationService(unittest.TestCase):

    @patch('backend.services.project_generation_service.requests')
    def test_generate_project_idea_success(self, mock_requests):
        mock_requests.post.return_value.status_code = 200
        mock_requests.post.return_value.json.return_value = {
            'choices': [{'text': 'Generated README content'}]
        }
        
        service = ProjectGenerationService()
        result = service.generate_project_idea('Python', ['machine learning'], ['TensorFlow', 'Keras'])
        
        self.assertEqual(result, 'Generated README content')

    @patch('backend.services.project_generation_service.requests.post')
    def test_generate_project_idea_api_error(self, mock_post):
        mock_post.side_effect = requests.RequestException('API error')
        service = ProjectGenerationService()
        result = service.generate_project_idea('Python', ['machine learning'], ['TensorFlow', 'Keras'])
        self.assertEqual(result, 'Failed to generate README due to API error.')


    @patch('backend.services.project_generation_service.requests')
    @patch('backend.services.project_generation_service.os')  
    @patch('backend.services.project_generation_service.subprocess')
    def test_create_repository_success(self, mock_subprocess, mock_os, mock_requests):
        mock_requests.post.return_value.status_code = 201
        mock_requests.post.return_value.json.return_value = {'html_url': 'https://github.com/user/new-repo'}
        
        service = ProjectGenerationService()
        result = service.create_repository('new-repo', 'README content', 'token123')
        
        self.assertEqual(result, 'https://github.com/user/new-repo')
        mock_os.makedirs.assert_called_once_with('./new-repo', exist_ok=True)
        mock_subprocess.run.assert_has_calls([
            call(['git', 'init'], check=True),
            call(['git', 'add', '.'], check=True),
            call(['git', 'commit', '-m', 'Initial commit with README and code'], check=True),
            call(['git', 'remote', 'add', 'origin', 'https://github.com/user/new-repo'], check=True),
            call(['git', 'push', '-u', 'origin', 'main'], check=True)
        ])

    @patch('backend.services.project_generation_service.requests')
    def test_create_repository_api_error(self, mock_requests):
        mock_requests.post.return_value.status_code = 500
        
        service = ProjectGenerationService()
        result = service.create_repository('new-repo', 'README', 'token')
        
        self.assertEqual(result, 'Failed to create repository')

