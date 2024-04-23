import { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Signup from './Signup';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'; // Import Navigate
import Login from './Login';
import Chat from './Chat';

function App() {
  const [authenticated, setAuthenticated] = useState(false);

  //Checks if user session is valid, stop url manipulation
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await fetch('/check-auth', {
          method: 'GET',
          credentials: 'include' // Include cookies in the request
        });
        if (response.ok) {
          setAuthenticated(true);
        } else {
          setAuthenticated(false);
        }
      } catch (error) {
        console.error('Error checking authentication:', error);
        setAuthenticated(false);
      }
    };

    checkAuth();
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path='/register' element={<Signup />} />
        <Route path='/login' element={<Login setAuthenticated={setAuthenticated} />} />
        <Route path='/chat' element={authenticated ? <Chat /> : <Navigate to='/login' />} />
        <Route path='/*' element={<Navigate to='/login' />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App;
