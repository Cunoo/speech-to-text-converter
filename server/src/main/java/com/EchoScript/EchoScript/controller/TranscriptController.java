package com.EchoScript.EchoScript.controller;

import com.EchoScript.EchoScript.DTO.transcript.TranscriptRequest;
import com.EchoScript.EchoScript.DTO.transcript.TranscriptResponse;
import com.EchoScript.EchoScript.service.TranscriptService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import com.EchoScript.EchoScript.config.AppConstants;

@RestController
@RequestMapping("/api/transcript")
@CrossOrigin(origins = AppConstants.FRONTEND_URL)
public class TranscriptController {

    @Autowired
    private TranscriptService transcriptService;

    @PostMapping("/request")
    public ResponseEntity<TranscriptResponse> requestTranscript(@RequestBody TranscriptRequest request) {

        try {
            // Call service to handle database operations
            TranscriptResponse response = transcriptService.processTranscriptRequest(
                    request.getUserID(),
                    request.getYoutubeUrl()
            );

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            // Handle errors
            TranscriptResponse errorResponse = new TranscriptResponse(
                    "Error processing request: " + e.getMessage(),
                    "error",
                    null
            );
            return ResponseEntity.badRequest().body(errorResponse);
        }
    }
}