//client/src/pages/transcript
// src/pages/Dashboard/Dashboard.js
import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

import { transcriptAPI } from '../../services/transcriptService';

const Transcript = () => {


    const navigate = useNavigate();
    const { user, logout, isAuthenticated } = useAuth();

    const [videoURL, setVideoURL] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        
        try {
            const response = await transcriptAPI.requestTranscript(user.id, videoURL);
            setResult(response);

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="min-h-screen bg-gray-900 py-20 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold text-white mb-4">
                        Welcome to Transcript
                    </h1>
                </div>
                
            </div>
            <div>
                <div class="mb-6">
                    <div class="flex justify-center">
                        <div class="w-1/2">
                            <label for="default-input" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white text-center">Default input</label>
                            <input type="text" id="videoURL"
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" 
                                onChange={(e) => setVideoURL(e.target.value)}
                                
                                />
                                
                        </div>
                    </div>
                    <div className='py-4 flex justify-center'>
                        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
                            onClick={handleSubmit}
                            disabled={loading || !videoURL}
                        >
                            {loading ? 'Processing...' : 'Submit'}
                        </button>
                    </div>
                </div>
            </div>
            <div class="bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-600 rounded-xl shadow-lg p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Video Processing Output</h3>
                    <span class="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full dark:bg-green-900 dark:text-green-300">
                        Ready
                    </span>
                </div>
                <div class="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-4 min-h-[250px] max-h-[400px] overflow-y-auto">
                    <pre class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap font-mono">
                        Video output text will appear here
                        <span class="text-gray-400">Waiting for video processing...</span>
                    </pre>
                </div>
            </div>
        </div>
    );
}


export default Transcript;