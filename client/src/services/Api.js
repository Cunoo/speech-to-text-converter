import { API_BASE_URL } from "../config.js";

// Function to get token from localStorage
const getAuthToken = () => {
    return localStorage.getItem('authToken');
};

// Function to set token into localStorage
const setAuthToken = (token) => {
    localStorage.setItem('authToken', token);
};

// Function to remove token from localStorage
const removeAuthToken = () => {
    localStorage.removeItem('authToken');
};

// Register a new user
export const registerUser = async (userData) => {
    const response = await fetch(`${API_BASE_URL}/users`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Registration failed');
    }
    
    return await response.json();
};

// User login
export const loginUser = async (credentials) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    });
    
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || 'Login failed');
    }
    
    const data = await response.json();
    
    // Store token in localStorage
    setAuthToken(data.token);
    
    return data;
};

// User logout
export const logoutUser = () => {
    removeAuthToken();
};

// Check if user is authenticated
export const isAuthenticated = () => {
    return getAuthToken() !== null;
};

// Fetch all users (protected route)
export const getAllUsers = async () => {
    const token = getAuthToken();
    
    const response = await fetch(`${API_BASE_URL}/users`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });
    
    if (!response.ok) {
        throw new Error('Failed to fetch users');
    }
    
    return await response.json();
};

// Decode JWT and get current user info
export const getCurrentUser = () => {
    const token = getAuthToken();
    if (!token) return null;
    
    try {
        // Decode JWT token (without signature verification – just to get the data)
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload;
    } catch (error) {
        console.error('Error decoding token:', error);
        return null;
    }
};

// Export token-related functions
export { getAuthToken, setAuthToken, removeAuthToken };
