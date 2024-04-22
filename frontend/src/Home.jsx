import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Home() {
    const [language, setLanguage] = useState('');
    const [skills, setSkills] = useState('');
    const [technologies, setTechnologies] = useState('');
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();

        // Pass form data via navigate to the Generation component
        navigate('/generation', { state: { language, skills, technologies } });
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
        </div>
    );
}

export default Home;
