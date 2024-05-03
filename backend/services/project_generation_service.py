from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import subprocess
from subprocess import CalledProcessError
from ..interfaces.project_service_interface import ProjectServiceInterface

load_dotenv()

app = Flask(__name__)
CORS(app)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class ProjectGenerationService(ProjectServiceInterface):
    def generate_project_idea(self, language, skills, technologies):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}'
        }
        prompt = (f"Create a comprehensive original README for a software project using {language}. " +
                  "The README should have a title\n" +  # Added newline for proper formatting
                  "The README should include an original idea that solves a problem or improves an existing project. " +
                  "The README should begin with an engaging introduction that explains the purpose of the project and its relevance. " +
                  f"Include detailed sections on the following: \n" +
                  "- **Project Goals**: Describe what the project aims to achieve and the problems it solves. \n" +
                  f"- **Technology Stack**: List all technologies like {technologies} used in the project and explain why each technology was chosen. \n" +
                  "- **Features**: Detail the key features and functionalities of the project. \n" +
                  "- **Setup Instructions**: Provide step-by-step instructions on how to get the project running locally, including environment setup, dependencies installation, and any necessary configurations. \n" +
                  "- **Usage**: Explain how to use the project, including examples of the commands or scripts to run. \n" +
                  "- **Contributing**: Outline how others can contribute to the project, mentioning any guidelines they need to follow. \n" +
                  f"Focus particularly on skills like {skills} when detailing features and contributions to emphasize how these capabilities are applied within the project.")
        try:
            response = requests.post(
                "https://api.openai.com/v1/completions",
                json={"model": "gpt-3.5-turbo-instruct", "prompt": prompt, "max_tokens": 1024, "temperature": 0.7, "top_p": 1, "frequency_penalty": 0, "presence_penalty": 0},
                headers=headers
            )
            response.raise_for_status()
            response_data = response.json()
            return response_data['choices'][0]['text'].strip()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return "Failed to generate README due to API error."

    def create_repository(self, repo_name, readme_content, token):
        headers = {'Authorization': f'token {token}'}
        data = {'name': repo_name}
        response = requests.post('https://api.github.com/user/repos', json=data, headers=headers)
        
        if response.status_code == 201:
            repo_url = response.json().get('html_url')
            if not repo_url:
                return jsonify({'error': 'GitHub repo URL not obtained'}), 500
            
            dir_path = os.path.abspath(repo_name)
            os.makedirs(dir_path, exist_ok=True)
            os.chdir(dir_path)
            
            try:
                subprocess.run(["git", "init"], check=True)
                with open('README.md', 'w') as file:
                    file.write(readme_content)
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", "Initial commit with README", "--no-verify"], check=True)
                
                subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
                # Check if remote main branch exists before pulling
                try:
                    subprocess.run(["git", "fetch"], check=True)
                    subprocess.run(["git", "pull", "origin", "main"], check=True)
                except subprocess.CalledProcessError:
                    print("No remote branch to pull from; skipping pull.")
                
                subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Git command failed: {e}")
                return jsonify({'error': 'Git command failed', 'details': str(e)}), 500
            finally:
                os.chdir("..")  # Return to original directory
            
            return jsonify({'repoUrl': repo_url})
        else:
            return jsonify({'error': 'Failed to create GitHub repository', 'status_code': response.status_code}), 500

project_service = ProjectGenerationService()

@app.route('/generate', methods=['POST'])
def generate_route():
    data = request.get_json()
    readme_content = project_service.generate_project_idea(data['language'], data['skills'], data['technologies'])
    return jsonify({'readme_content': readme_content})

@app.route('/create-repo', methods=['POST'])
def create_repo_route():
    data = request.get_json()
    repo_url = project_service.create_repository(data['repoName'], data['readmeContent'], data['gitHubToken'])
    return jsonify({'repoUrl': repo_url})

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', False), port=5001)
