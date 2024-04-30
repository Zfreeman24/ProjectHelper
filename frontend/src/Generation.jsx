import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import LinearProgress from '@mui/material/LinearProgress';

function Generation() {
    const location = useLocation();
    const [gitHubToken, setGitHubToken] = useState('');
    const [repoName, setRepoName] = useState('');
    const [revealedText, setRevealedText] = useState('');
    const [repoUrl, setRepoUrl] = useState('');
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        if (location.state) {
            setProgress(10);  // Initial progress for starting operation
            const { language, skills, technologies } = location.state;
            generateReadme(language, skills, technologies);
        }
    }, [location]);

    const generateReadme = async (language, skills, technologies) => {
        const apiUrl = 'http://localhost:5001/generate';
        setProgress(20); // Set progress as generation starts
        try {
            const response = await axios.post(apiUrl, { language, skills, technologies });
            setRevealedText(response.data.readme_content);
            setProgress(100); // Set halfway when generation is done
            setTimeout(() => {
                setProgress(0);
                setShowProgress(false); 
            }, 2000);
        } catch (error) {
            console.error('Error generating project idea:', error);
            alert('Failed to generate project idea. Please try again.');
        }
    };

    const handleRepoCreation = async (e) => {
        e.preventDefault();
        if (!gitHubToken || !repoName || !revealedText) {
            alert('Please enter GitHub token, repository name, and generate README before creating repository.');
            return;
        }
        const apiUrl = 'http://localhost:5001/create-repo';
        try {
            const response = await axios.post(apiUrl, {
                gitHubToken,
                repoName,
                readmeContent: revealedText
            });
            if (response.data.repoUrl) {
                setRepoUrl(response.data.repoUrl);
            } else {
                alert('Failed to create GitHub repository. Please check the provided GitHub token and try again.');
            }
        } catch (error) {
            console.error('Error creating GitHub repository:', error);
            alert('Failed to create GitHub repository. Please check the provided GitHub token and try again.');
        }
    };
    
    return (
        <div className="container mt-5">
            <h2>Generate Project Idea</h2>
            <LinearProgress variant="determinate" value={progress} />
            {revealedText && (
                <div>
                    <ReactMarkdown>{revealedText}</ReactMarkdown>
                    <form onSubmit={(e) => e.preventDefault()}>
                        <input
                            type="text"
                            value={repoName}
                            onChange={e => setRepoName(e.target.value)}
                            placeholder="Enter your Repository Name"
                        />
                        <input
                            type="text"
                            value={gitHubToken}
                            onChange={e => setGitHubToken(e.target.value)}
                            placeholder="Enter your GitHub token here"
                        />
                        <button onClick={handleRepoCreation}>Create GitHub Repository</button>
                    </form>
                </div>
            )}
            {repoUrl && <p>Repository created successfully: <a href={repoUrl} target="_blank" rel="noopener noreferrer">{repoUrl}</a></p>}
        </div>
    );
}

export default Generation;
