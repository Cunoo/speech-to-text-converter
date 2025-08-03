package com.EchoScript.EchoScript.service;

import com.EchoScript.EchoScript.DTO.transcript.TranscriptResponse;
import com.EchoScript.EchoScript.entity.UserVideoRequest;
import com.EchoScript.EchoScript.entity.Video;
import com.EchoScript.EchoScript.repository.UserVideoRequestRepository;
import com.EchoScript.EchoScript.repository.VideoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Optional;

@Service
public class TranscriptService {
    @Autowired
    private VideoRepository videoRepository;

    @Autowired
    private UserVideoRequestRepository userVideoRequestRepository;

    public TranscriptResponse processTranscriptRequest(Long userID, String youtubeUrl) {
        //check if video already exists
        Optional<Video> existingVideo = videoRepository.findByYoutubeUrl(youtubeUrl);

        Video video;
        if(existingVideo.isPresent()) {
            video = existingVideo.get();
        } else {
            video = new Video();
            video.setYoutubeUrl(youtubeUrl);
            video.setStatus("pending");
            video = videoRepository.save(video);
        }

        // check if user already requested this video
        if(!userVideoRequestRepository.existsByUserIdAndVideoId(userID, video.getId())){
            //Create user request record
            UserVideoRequest request = new UserVideoRequest();
            request.setUserId(userID);
            request.setVideoId(video.getId());
            request.setRequestedAt(LocalDateTime.now());
            userVideoRequestRepository.save(request);
        }
        return new TranscriptResponse("Request submitted successfully", "pending", video.getId());
    }
}
