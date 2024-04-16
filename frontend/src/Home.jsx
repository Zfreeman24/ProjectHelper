import React, { useState } from 'react';
import axios from 'axios';

function Home() {
    const [language, setLanguage] = useState('');
    const [skills, setSkills] = useState('');
    const [technologies, setTechnologies] = useState('');
    const [projectIdea, setProjectIdea] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Chat GPT API or any relevant API URL and data structure
        const apiUrl = 'YOUR_CHAT_GPT_API_URL';
        const postData = {
            language,
            skills,
            technologies
        };

        try {
            const response = await axios.post(apiUrl, postData);
            setProjectIdea(response.data); // Assuming the API returns a structured project idea
        } catch (error) {
            console.error('Error fetching project ideas:', error);
            alert('Failed to fetch project ideas');
        }
    };

    return (
        <div className="container mt-5">
            <h2>Project Idea Generator</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label htmlFor="language" className="form-label">Preferred Programming Language</label>
                    <select id="language" className="form-select" value={language} onChange={e => setLanguage(e.target.value)}>
                        <option value="">Select a Language</option>
                        <option value="Python">Python</option>
                        <option value="JavaScript">JavaScript</option>
                        <option value="Java">Java</option>
                        <option value="C#">C#</option>
                        <option value="C++">C++</option>
                    </select>
                </div>
                <div className="mb-3">
                    <label htmlFor="skills" className="form-label">Skills to Develop</label>
                    <input type="text" id="skills" className="form-control" placeholder="e.g., Web Development, Machine Learning" value={skills} onChange={e => setSkills(e.target.value)} />
                </div>
                <div className="mb-3">
                    <label htmlFor="technologies" className="form-label">Technologies to Use</label>
                    <input type="text" id="technologies" className="form-control" placeholder="e.g., React, Docker, TensorFlow" value={technologies} onChange={e => setTechnologies(e.target.value)} />
                </div>
                <button type="submit" className="btn btn-primary">Generate Project Idea</button>
            </form>

            {projectIdea && (
                <div className="mt-4">
                    <h3>Project Idea: {projectIdea.title}</h3>
                    <p><strong>Description:</strong> {projectIdea.description}</p>
                    <p><strong>Recommended Languages:</strong> {projectIdea.languages.join(', ')}</p>
                    <p><strong>Technologies Needed:</strong> {projectIdea.technologies.join(', ')}</p>
                </div>
            )}
        </div>
    );
}

export default Home;
