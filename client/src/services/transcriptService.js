import { API_BASE_URL } from "../config.js";


export const transcriptAPI = {
    
    async requestTranscript(userID, youtubeUrl) {
        const response = await fetch(`${API_BASE_URL}/transcript/request`, {
            method: 'POST',
            headers: {'Content-Type' : 'application/json'},
            body: JSON.stringify({userID, youtubeUrl})
        });
        if (!response.ok) {
            throw new Error(`Error requesting transcript: ${response.statusText}`);
        }
        return response.json();
    }
}