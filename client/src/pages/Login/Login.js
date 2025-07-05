//src/pages/Login/Login.js

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { Link } from 'react-router-dom';




const Login = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });


    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {

        } catch (error) {
            console.error('Login failed:', error);
        }
    }

return (
<div style={{ maxWidth: '400px', margin: '50px auto', paddingTop: '120px' }}>
    <h1>Login</h1>
    
    <form onSubmit={handleSubmit}>
    <div style={{ marginBottom: '15px', paddingTop: '120px' }}>
        <label>Email:</label>
        <input
        type="email"
        name="email"
        value={formData.email}
        onChange={handleChange}
        style={{ 
            width: '100%', 
            padding: '8px', 
            margin: '5px 0' 
        }}
        required
        />
    </div>

    <div style={{ marginBottom: '15px' }}>
        <label>password:</label>
        <input
        type="password"
        name="password"
        value={formData.password}
        onChange={handleChange}
        style={{ 
            width: '100%', 
            padding: '8px', 
            margin: '5px 0' 
        }}
        required
        />
    </div>

    <button 
        type="submit"
        style={{
        width: '100%',
        padding: '10px',
        backgroundColor: '#007bff',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer'
        
        }}
    >
        Login in
    </button>
    </form>

    <p style={{ marginTop: '20px', textAlign: 'center' }}>
    No account <Link to="/register">Register</Link>
    </p>
</div>
);
};

export default Login;