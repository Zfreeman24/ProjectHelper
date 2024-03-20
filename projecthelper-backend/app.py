from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/generate-project', methods=['POST'])
def generate_project():
    data = request.json
    skills = data.get('skills')
    difficulty = data.get('difficulty')
    additional_info = data.get('additionalInfo', 'None provided')

    # Mock response for demonstration. This is where you'd implement your logic.
    project_idea = {
        'title': f"A {difficulty} project to improve your {skills}",
        'description': f"This project is designed to enhance your skills in {skills}. Additional info: {additional_info}"
    }

    return jsonify(project_idea)

if __name__ == '__main__':
    app.run(debug=True)
