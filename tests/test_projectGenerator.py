import unittest
from backend.projectGenerator import generate_idea_with_gpt, create_github_repo

class TestProjectGenerator(unittest.TestCase):

    def test_generate_idea_with_gpt_success(self):
        language = "Python"
        skills = "machine learning, data analysis" 
        technologies = "pandas, sklearn, tensorflow"
        readme = generate_idea_with_gpt(language, skills, technologies)
        self.assertIsInstance(readme, str)
        self.assertGreater(len(readme), 50)

    def test_generate_idea_with_gpt_failure(self):
        language = "Python"
        skills = "machine learning, data analysis"
        technologies = "pandas, sklearn, tensorflow"        
        readme = generate_idea_with_gpt(language, skills, technologies)
        self.assertNotIsInstance(readme, dict)

    def test_create_github_repo_success(self):
        token = "validtoken123"
        readme_content = "# My Project"
        repo_url = create_github_repo("Test Repo", readme_content, token)
        self.assertIsInstance(repo_url, str)
        self.assertTrue(repo_url.startswith("https://github.com/"))

    def test_create_github_repo_failure(self):
        token = "invalidtoken"
        readme_content = "# My Project"
        repo_url = create_github_repo("Test Repo", readme_content, token)
        self.assertIsInstance(repo_url, str)
        self.assertEqual(repo_url, "Failed to create repository")

if __name__ == '__main__':
    unittest.main()
