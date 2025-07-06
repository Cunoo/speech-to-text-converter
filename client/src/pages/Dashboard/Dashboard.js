// src/pages/Dashboard/Dashboard.js
import React from 'react';
import { useAuth } from '../../contexts/AuthContext';

const Dashboard = () => {
    const { user } = useAuth();

    return (
        <div className="min-h-screen bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold text-white mb-4">
                        Welcome to Dashboard
                    </h1>
                    <p className="text-xl text-gray-300">
                        Hello, {user?.user?.username || user?.username}!
                    </p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                        <h3 className="text-xl font-semibold text-white mb-2">
                            User Management
                        </h3>
                        <p className="text-gray-300 mb-4">
                            Manage your user accounts and profiles
                        </p>
                        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md">
                            View Users
                        </button>
                    </div>
                    
                    <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                        <h3 className="text-xl font-semibold text-white mb-2">
                            Content Manager
                        </h3>
                        <p className="text-gray-300 mb-4">
                            Create and manage your content
                        </p>
                        <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md">
                            Manage Content
                        </button>
                    </div>
                    
                    <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                        <h3 className="text-xl font-semibold text-white mb-2">
                            Analytics
                        </h3>
                        <p className="text-gray-300 mb-4">
                            View your application statistics
                        </p>
                        <button className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md">
                            View Analytics
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;