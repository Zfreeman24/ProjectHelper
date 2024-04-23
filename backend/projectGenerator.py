from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import subprocess

app = Flask(__name__)
CORS(app)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

@app.route('/generate', methods=['POST'])
def generate_project():
    data = request.get_json()
    readme_content = generate_idea_with_gpt(data['language'], data['skills'], data['technologies'])
    return jsonify({'readme_content': readme_content})

@app.route('/create-repo', methods=['POST'])
def create_repository():
    data = request.get_json()
    token = data['gitHubToken']
    readme_content = data['readmeContent']
    repo_url = create_github_repo("New Project", readme_content, token)
    return jsonify({'repoUrl': repo_url})

def generate_idea_with_gpt(language, skills, technologies):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    prompt = (
        f"Create a comprehensive README for a software project using {language}. "
        f"The README should begin with an engaging introduction that explains the purpose of the project and its relevance. "
        f"Include detailed sections on the following: \n"
        f"- **Project Goals**: Describe what the project aims to achieve and the problems it solves. \n"
        f"- **Technology Stack**: List all technologies like {technologies} used in the project and explain why each technology was chosen. \n"
        f"- **Features**: Detail the key features and functionalities of the project. \n"
        f"- **Setup Instructions**: Provide step-by-step instructions on how to get the project running locally, including environment setup, dependencies installation, and any necessary configurations. \n"
        f"- **Usage**: Explain how to use the project, including examples of the commands or scripts to run. \n"
        f"- **Contributing**: Outline how others can contribute to the project, mentioning any guidelines they need to follow. \n"
        f"- **License**: Specify the type of license under which the project is released. \n"
        f"- **Credits and Acknowledgements**: Give credit to any individuals, organizations, or resources that were instrumental in the development of the project. \n"
        f"Focus particularly on skills like {skills} when detailing features and contributions to emphasize how these capabilities are applied within the project."
    )

    try:
        response = requests.post(
            "https://api.openai.com/v1/completions",
            json={
                "model": "gpt-3.5-turbo-instruct",
                "prompt": prompt,
                "max_tokens": 1024,
                "temperature": 0.7,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0
            },
            headers=headers
        )
        response.raise_for_status()
        response_data = response.json()
        return response_data['choices'][0]['text'].strip()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return "Failed to generate README due to API error."

def create_github_repo(repo_name, readme_content, token):
    headers = {'Authorization': f'token {token}'}
    data = {'name': repo_name}
    response = requests.post('https://api.github.com/user/repos', json=data, headers=headers)

    if response.status_code == 201:
        repo_url = response.json().get('html_url')
        # Setup local directory for git operations
        dir_path = f"./{repo_name}"
        os.makedirs(dir_path, exist_ok=True)
        os.chdir(dir_path)

        # Initialize local git repository
        subprocess.run(["git", "init"], check=True)

        # Create README.md and write content
        with open('README.md', 'w') as file:
            file.write(readme_content)

        # Git operations
        subprocess.run(["git", "add", "README.md"], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit with README"], check=True)

        # Add remote repository URL and push to GitHub
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

        # Change back to the original directory
        os.chdir("..")
        
        return repo_url
    else:
        return "Failed to create repository"

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', False), port=5001)
