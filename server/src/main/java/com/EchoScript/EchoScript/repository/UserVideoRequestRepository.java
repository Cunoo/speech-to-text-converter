package com.EchoScript.EchoScript.repository;

import com.EchoScript.EchoScript.entity.UserVideoRequest;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserVideoRequestRepository extends JpaRepository<UserVideoRequest, Long> {
    boolean existsByUserIdAndVideoId(Long userId, Long videoId);
}
