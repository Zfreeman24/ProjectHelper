import unittest
from unittest.mock import patch

from project_generation_service import project_service

class TestProjectGenerationService(unittest.TestCase):

    @patch('project_generation_service.requests.post')
    def test_generate_project_idea_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'choices': [{'text': 'Generated README content'}]
        }
        
        language = 'Python'
        skills = 'data analysis, machine learning'
        technologies = 'pandas, scikit-learn'
        readme = project_service.generate_project_idea(language, skills, technologies)
        
        self.assertEqual(readme, 'Generated README content')

    @patch('project_generation_service.requests.post')  
    def test_generate_project_idea_api_error(self, mock_post):
        mock_post.side_effect = Exception('API error')
        
        language = 'Python'
        skills = 'web scraping'
        technologies = 'BeautifulSoup'
        readme = project_service.generate_project_idea(language, skills, technologies)

        self.assertEqual(readme, 'Failed to generate README due to API error.')

    @patch('project_generation_service.requests.post')
    @patch('project_generation_service.subprocess.run')
    @patch('project_generation_service.os.makedirs')  
    def test_create_repository_success(self, mock_makedirs, mock_run, mock_post):
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {'html_url': 'https://github.com/user/new-repo'}
        
        repo_url = project_service.create_repository('new-repo', 'README content', 'token123')
        
        self.assertEqual(repo_url, 'https://github.com/user/new-repo')
        mock_makedirs.assert_called_once_with('./new-repo', exist_ok=True)
        mock_run.assert_called()

    @patch('project_generation_service.requests.post')
    def test_create_repository_api_error(self, mock_post):
        mock_post.return_value.status_code = 500
        
        repo_url = project_service.create_repository('new-repo', 'README content', 'token123')
        
        self.assertEqual(repo_url, 'Failed to create repository')

