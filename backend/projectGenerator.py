from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

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
    prompt = f"Create a comprehensive README for a project using {language}, focusing on {skills} and incorporating technologies like {technologies}. The README should include an introduction, project goals, technology stack, and setup instructions."

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json={
                "model": "text-davinci-003",
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
        # Additional code to push the README.md can be added here.
        return repo_url
    else:
        return "Failed to create repository"

if __name__ == '__main__':
    app.run(debug=True, port = 5001)
