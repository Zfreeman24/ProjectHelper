import React, { useState } from 'react';
import './App.css';

function App() {
  const [formState, setFormState] = useState({
    skills: '',
    difficulty: '',
    additionalInfo: '',
  });

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
        <h2>Welcome to Project Helper!</h2>
        <form onSubmit={handleSubmit} className="form">
          <div className="input-group">
            <label>Skills You Want to Improve:</label>
            <input type="text" name="skills" value={formState.skills} onChange={handleChange} />
          </div>
          <div className="input-group">
            <label>Difficulty Level:</label>
            <select name="difficulty" value={formState.difficulty} onChange={handleChange}>
              <option value="">Select Difficulty</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>
          <div className="input-group">
            <label>Additional Info (optional):</label>
            <textarea name="additionalInfo" value={formState.additionalInfo} onChange={handleChange}></textarea>
          </div>
          <button type="submit">Generate Project Idea</button>
        </form>
      </header>
    </div>
  );
}

export default App;
