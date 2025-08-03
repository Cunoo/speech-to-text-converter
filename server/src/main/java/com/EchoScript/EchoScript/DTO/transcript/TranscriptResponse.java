package com.EchoScript.EchoScript.DTO.transcript;

public class TranscriptResponse {
    private String message;
    private String status;
    private Long videoId;
    private String transcription;  // null if still pending

    // Constructors
    public TranscriptResponse() {}

    public TranscriptResponse(String message, String status, Long videoId) {
        this.message = message;
        this.status = status;
        this.videoId = videoId;
    }

    public TranscriptResponse(String message, String status, Long videoId, String transcription) {
        this.message = message;
        this.status = status;
        this.videoId = videoId;
        this.transcription = transcription;
    }

    // Getters and setters
    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public Long getVideoId() { return videoId; }
    public void setVideoId(Long videoId) { this.videoId = videoId; }

    public String getTranscription() { return transcription; }
    public void setTranscription(String transcription) { this.transcription = transcription; }
}