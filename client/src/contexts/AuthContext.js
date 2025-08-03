import React, { createContext, useContext, useState, useEffect } from 'react';
import { getAuthToken, removeAuthToken } from '../services/Api';

const AuthContext = createContext();

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = getAuthToken();
        const savedUserData = localStorage.getItem('userData');
        
        if (token && savedUserData) {
            try {
                const payload = JSON.parse(atob(token.split('.')[1]));
                const currentTime = Date.now() / 1000;
                
                if (payload.exp > currentTime) {
                    const userData = JSON.parse(savedUserData);
                    // Extract the nested user object
                    setUser(userData.user); 
                } else {
                    removeAuthToken();
                    localStorage.removeItem('userData');
                }
            } catch (error) {
                console.error('Error parsing token:', error);
                removeAuthToken();
                localStorage.removeItem('userData');
            }
        }
        setLoading(false);
    }, []);

    const login = (userData) => {
        setUser(userData.user);
        // Store complete user data in localStorage
        localStorage.setItem('userData', JSON.stringify(userData));
    };

    const logout = () => {
        setUser(null);
        removeAuthToken();
        localStorage.removeItem('userData');  
    };

    const value = {
        user,
        login,
        logout,
        loading,
        isAuthenticated: !!user
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};


export default AuthContext;