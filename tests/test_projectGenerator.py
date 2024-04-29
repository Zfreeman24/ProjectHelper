import unittest
from unittest.mock import patch

from backend.projectGenerator import generate_idea_with_gpt, create_github_repo

class ProjectGeneratorTestCase(unittest.TestCase):

    @patch('backend.projectGenerator.requests') 
    def test_generate_idea_with_gpt_success(self, mock_requests):
        mock_requests.post.return_value.status_code = 200
        mock_requests.post.return_value.json.return_value = {'choices': [{'text': 'Test README'}]}
        
        readme = generate_idea_with_gpt('Python', 'machine learning, data analysis', 'TensorFlow, Pandas')
        
        self.assertEqual(readme, 'Test README')

    @patch('backend.projectGenerator.requests')
    def test_generate_idea_with_gpt_api_error(self, mock_requests):
        mock_requests.post.side_effect = Exception('API Error')
        
        readme = generate_idea_with_gpt('Python', 'machine learning, data analysis', 'TensorFlow, Pandas')

        self.assertEqual(readme, 'Failed to generate README due to API error.')

    @patch('backend.projectGenerator.requests')
    @patch('backend.projectGenerator.subprocess')
    def test_create_github_repo_success(self, mock_subprocess, mock_requests):
        mock_requests.post.return_value.status_code = 201
        mock_requests.post.return_value.json.return_value = {'html_url': 'https://github.com/test/repo'}
        
        repo_url = create_github_repo('TestRepo', 'README', 'testtoken')
        
        self.assertEqual(repo_url, 'https://github.com/test/repo')

    @patch('backend.projectGenerator.requests')
    def test_create_github_repo_api_error(self, mock_requests):
        mock_requests.post.return_value.status_code = 500
        
        repo_url = create_github_repo('TestRepo', 'README', 'testtoken')

        self.assertEqual(repo_url, 'Failed to create repository')

