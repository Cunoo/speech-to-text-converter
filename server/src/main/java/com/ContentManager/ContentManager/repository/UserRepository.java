package com.ContentManager.ContentManager.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.ContentManager.ContentManager.entity.User;

public interface  UserRepository extends JpaRepository<User, Long> {
    
    Optional<User> findByUsername(String username);
    
    Optional<User> findByEmail(String email);
    
    List<User> findAllByOrderByCreatedAtDesc();
    
    boolean existsByUsername(String username);
    
    boolean existsByEmail(String email);
    
}
