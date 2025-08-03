package com.EchoScript.EchoScript.DTO.transcript;


public class TranscriptRequest {
    private Long userID;
    private String youtubeUrl;

    // Default constructor
    public TranscriptRequest() {}

    // Constructor with parameters
    public TranscriptRequest(Long userID, String youtubeUrl) {
        this.userID = userID;
        this.youtubeUrl = youtubeUrl;
    }

    // Getters and setters
    public Long getUserID() {
        return userID;
    }

    public void setUserID(Long userID) {
        this.userID = userID;
    }

    public String getYoutubeUrl() {
        return youtubeUrl;
    }

    public void setYoutubeUrl(String youtubeUrl) {
        this.youtubeUrl = youtubeUrl;
    }
}