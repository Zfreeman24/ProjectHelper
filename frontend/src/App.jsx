import { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Signup from './Signup';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';
import Home from './Home';
import Generation from './Generation';

function App() {
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      try{
        const response = await fetch('/check_auth');
        const data = await response.json()
        setAuthenticated(data.authenticated);
      }catch(err){
        console.log('Error checking authentication:', err);
        setAuthenticated(false);
      }
    };

    checkAuth();
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path='/register' element={<Signup />}></Route>
        <Route path='/login' element={<Login setAuthenticated={setAuthenticated} />}></Route>
        <Route path='/home' element={authenticated ? <Home /> : <Navigate to='/login' />}></Route>
        <Route path='/generation' element={authenticated ? <Generation/>: <Navigate to='/login' />}> </Route>
        <Route path='/*' element={<Navigate to='/login' />}> </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
