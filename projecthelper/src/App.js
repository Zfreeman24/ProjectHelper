import React, { useState } from 'react';
import './App.css';

//Test

function App() {
  const [formState, setFormState] = useState({
    skills: '',
    difficulty: '',
    additionalInfo: '',
  });

  const [currentPage, setCurrentPage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormState(prevState => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('http://localhost:5000/generate-project', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formState),
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      // Display the generated project idea to the user
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };
  

  return (
    <div className="App">
      <header className="App-header">
        <h2>NaviProject</h2>
        <p>🚀 A Project Helper designed to help Computer Science students learn and grow.</p>
      </header>
      <div className="navbar">
      <a1 href="#home" className={`home-link ${currentPage === 'home' ? 'active' : ''}`} onClick={() => setCurrentPage('home')}>NaviProject</a1>
        <div className="nav-links">
          <a href="#login" className={currentPage === 'login' ? 'active' : ''} onClick={() => setCurrentPage('login')}>Login</a>
          <a href="#signup" className={currentPage === 'signup' ? 'active' : ''} onClick={() => setCurrentPage('signup')}>Signup</a>
          <a href="#team" className={currentPage === 'team' ? 'active' : ''} onClick={() => setCurrentPage('team')}>Team</a>
        </div>
      </div>
    </div>
  );
}

export default App;
