import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';  // Import useLocation from 'react-router-dom'

function Generation() {
    const location = useLocation();
    const [language, setLanguage] = useState('');
    const [skills, setSkills] = useState('');
    const [technologies, setTechnologies] = useState('');
    const [gitHubToken, setGitHubToken] = useState('');  // Ensure gitHubToken's initial state
    const [revealedText, setRevealedText] = useState('');
    const [repoUrl, setRepoUrl] = useState('');

    useEffect(() => {
        if (location.state) {
            const { language, skills, technologies } = location.state;
            setLanguage(language);
            setSkills(skills);
            setTechnologies(technologies);
            generateReadme(language, skills, technologies);
        }
    }, [location]);

    const generateReadme = async (language, skills, technologies) => {
        const apiUrl = 'http://localhost:5001/generate';  // Adjust as necessary
        try {
            const response = await axios.post(apiUrl, { language, skills, technologies });
            revealText(response.data.readme_content);
        } catch (error) {
            console.error('Error generating project idea:', error);
            alert('Failed to generate project idea. Please try again.');
        }
    };

    const handleRepoCreation = async (e) => {
        e.preventDefault();
        const apiUrl = 'http://localhost:5001/create-repo';  // Adjust as necessary

        try {
            const response = await axios.post(apiUrl, {
                gitHubToken,
                readmeContent: revealedText
            });
            setRepoUrl(response.data.repoUrl);
        } catch (error) {
            console.error('Error creating GitHub repository:', error);
            alert('Failed to create GitHub repository. Please check the provided GitHub token and try again.');
        }
    };

    const revealText = (text) => {
        const speed = 50;  // Speed in milliseconds
        let index = 0;
        let textSoFar = '';

        const intervalId = setInterval(() => {
            if (index < text.length) {
                textSoFar += text.charAt(index);
                setRevealedText(textSoFar);
                index++;
            } else {
                clearInterval(intervalId);
            }
        }, speed);
    };

    return (
        <div className="container mt-5">
            <h2>Generate Project Idea</h2>
            {/* Display any form inputs or controls if necessary */}
            {revealedText && (
                <div>
                    <pre>{revealedText}</pre>
                    <form onSubmit={handleRepoCreation}>
                        <input
                            type="text"
                            value={gitHubToken}
                            onChange={e => setGitHubToken(e.target.value)}
                            placeholder="Enter your GitHub token here"
                        />
                        <button type="submit">Create GitHub Repository</button>
                    </form>
                </div>
            )}
            {repoUrl && <p>Repository created successfully: <a href={repoUrl} target="_blank" rel="noopener noreferrer">{repoUrl}</a></p>}
        </div>
    );
}

export default Generation;
