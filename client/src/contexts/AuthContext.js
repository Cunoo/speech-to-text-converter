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
        // Check if user is logged in on app load
        const token = getAuthToken();
        if (token) {
            try {
                // Decode JWT token to extract user data
                const payload = JSON.parse(atob(token.split('.')[1]));
                
                // Check token expiration time
                const currentTime = Date.now() / 1000;
                if (payload.exp > currentTime) {
                    setUser({
                        username: payload.sub,
                        token: token
                    });
                } else {
                    // Token has expired, remove it
                    removeAuthToken();
                }
            } catch (error) {
                console.error('Error parsing token:', error);
                removeAuthToken();
            }
        }
        setLoading(false);
    }, []);

    const login = (userData) => {
        setUser(userData);
    };

    const logout = () => {
        setUser(null);
        removeAuthToken();
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