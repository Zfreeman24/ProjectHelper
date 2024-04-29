from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import subprocess
from ..interfaces.project_service_interface import ProjectServiceInterface

app = Flask(__name__)
CORS(app)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class ProjectGenerationService(ProjectServiceInterface):
    def generate_project_idea(self, language, skills, technologies):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}'
        }
        prompt = (f"Create a comprehensive README for a software project using {language}. " +
                  "The README should begin with an engaging introduction that explains the purpose of the project and its relevance. " +
                  f"Include detailed sections on the following: \n" +
                  "- **Project Goals**: Describe what the project aims to achieve and the problems it solves. \n" +
                  f"- **Technology Stack**: List all technologies like {technologies} used in the project and explain why each technology was chosen. \n" +
                  "- **Features**: Detail the key features and functionalities of the project. \n" +
                  "- **Setup Instructions**: Provide step-by-step instructions on how to get the project running locally, including environment setup, dependencies installation, and any necessary configurations. \n" +
                  "- **Usage**: Explain how to use the project, including examples of the commands or scripts to run. \n" +
                  "- **Contributing**: Outline how others can contribute to the project, mentioning any guidelines they need to follow. \n" +
                  "- **License**: Specify the type of license under which the project is released. \n" +
                  "- **Credits and Acknowledgements**: Give credit to any individuals, organizations, or resources that were instrumental in the development of the project. \n" +
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
            dir_path = f"./{repo_name}"
            os.makedirs(dir_path, exist_ok=True)
            os.chdir(dir_path)
            subprocess.run(["git", "init"], check=True)
            with open('README.md', 'w') as file:
                file.write(readme_content)
            subprocess.run(["git", "add", "README.md"], check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit with README"], check=True)
            subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            os.chdir("..")
            return repo_url
        else:
            return "Failed to create repository"

project_service = ProjectGenerationService()

@app.route('/generate', methods=['POST'])
def generate_route():
    data = request.get_json()
    readme_content = project_service.generate_project_idea(data['language'], data['skills'], data['technologies'])
    return jsonify({'readme_content': readme_content})

@app.route('/create-repo', methods=['POST'])
def create_repo_route():
    data = request.get_json()
    repo_url = project_service.create_repository("New Project", data['readmeContent'], data['gitHubToken'])
    return jsonify({'repoUrl': repo_url})

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', False), port=5001)
