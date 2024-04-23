import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [parameters, setParameters] = useState({
    language: '',
    difficulty: '',
    topic: '',
    info: ''
  });
  const [response, setResponse] = useState('');

  const handleChange = (e) => {
    setParameters({ ...parameters, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (parameters.language.trim() === '' || parameters.difficulty.trim() === '' || parameters.topic.trim() === '' || parameters.info.trim() === '') {
      alert('Please fill in all fields');
      return;
    }

    try {
      const res = await axios.post('http://localhost:3001/chat', parameters);
      setResponse(res.data.response);
    } catch (err) {
      console.error('Chat error:', err);
    }
  };

  const handleLogout = async () => {
    try{
      const res = await axios.get('http://localhost:3001/logout');
      window.location.href = '/login';
    }catch(err){
      console.error('Logout Error', err);
    }
  } 

  return (
    <div>
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">Project Generator</a>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
              <a class="nav-link" href="#">Profile</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Saved</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Github</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#" onClick={handleLogout}>Logout</a>
            </li>

          </ul>
        </div>
      </nav>

      <div className="d-flex justify-content-center align-items-center bg-secondary vh-100">
        <div className="bg-white p-3 rounded w-25">

          <h2>Project Details</h2>

          <form onSubmit={handleSubmit}>
            <div className='mb-3'>
              <label><strong>Programming Language</strong></label>
              <input 
                type='text'
                placeholder ="Enter Langauge"
                autoComplete="off"
                name="language"
                value={parameters.language}
                className="form-control rounded-0"
                onChange={handleChange}
              />
            </div>

            <div className='mb-3'>
              <label><strong>Difficulty Level</strong></label>
              <input 
                type='text'
                placeholder='Enter easy, medium, or hard'
                autoComplete='off'
                name='difficulty'
                value={parameters.difficulty}
                className='form-control rounded-0'
                onChange={handleChange}
              />
            </div>

            <div className='mb-3'>
              <label><strong>Topic</strong></label>
              <input 
                type='text'
                placeholder='Enter topic (EX. array)'
                autoComplete='off'
                name='topic'
                value={parameters.topic}
                className='form-control rounded-0'
                onChange={handleChange}
              />
            </div>

            <div className='mb-3'>
              <label><strong>Additional Info</strong></label>
              <input 
                type='text'
                placeholder='Enter info (EX. is game-based)'
                autoComplete='off'
                name='info'
                value={parameters.info}
                className='form-control rounded-0'
                onChange={handleChange}
              />
            </div>

            <button type="submit" className="btn btn-success w-100 rounded-0">Find</button>
          </form>
        </div>

        <div className='col-2'></div>

        <div className='bg-white p-3 rounded w-50'>
          {response && (
            <div> 
              <h2>Response:</h2>
              <p>{response}</p>
            </div>
          )}
          <button>Save</button>
        </div>

      </div>
    </div>
  );
}

export default App;
