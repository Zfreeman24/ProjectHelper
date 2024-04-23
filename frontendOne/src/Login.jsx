import React from "react";
import { useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Login(){
    const [email, setEmail] = useState();
    const [password, setPassword] = useState();
    const [errorE, setErrorE] = useState();
    const [errorP, setErrorP] = useState();
    const navigate = useNavigate();

    const handleSubmit = (e) =>{
        e.preventDefault();
        setErrorE("");
        setErrorP("");

        axios.post('http://localhost:3001/login', {email, password})
            .then(result => {
                console.log(result);

                if (result.data === "Success"){
                    navigate('/chat');
                }else if (result.data === "Wrong password"){
                    setErrorP("Invalid password");
                }else{
                    setErrorE("Invalid email");
                }
            }).catch(err => console.log(err));
    }

    return(
        <div className="d-flex justify-content-center align-items-center bg-secondary vh-100">
            <div className="bg-white p-3 rounded w-25">
                <h2>Login</h2>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label htmlFor="email"> <strong>Email</strong> </label>
                        <input 
                            type="email"
                            placeholder="Enter email"
                            autoComplete="off"
                            name="email"
                            className="form-control rounded-0"
                            onChange={(e) => setEmail(e.target.value)}
                        />
                        {errorE && <div className="text-danger text-center text-strong">{errorE}</div>}
                    </div>

                    <div className="mb-3">
                        <label htmlFor="password"> <strong>Password</strong> </label>
                        <input 
                            type="password"
                            placeholder="Enter password"
                            name="password"
                            className="form-control rounded-0"
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        {errorP && <div className="text-danger text-center text-strong">{errorP}</div>}
                    </div>
                    
                    <button type="submit" className="btn btn-primary w-100 rounded-0 mt-2">Login</button>
                </form>

                <p>Don't Have an Account</p>
                <Link to='/register' className="btn btn-default border w-100 bg-light rounded-0 text-decoration-none">Sign Up</Link>
            </div>
        </div>
    )
}

export default Login;