package com.EchoScript.EchoScript.service;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import com.EchoScript.EchoScript.entity.User;
import com.EchoScript.EchoScript.repository.UserRepository;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    private BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    //Create
    public User createUser(User user) {
        //validate username and email dont exist
        if (userRepository.existsByUsername(user.getUsername())) {
            throw new RuntimeException("Username already exists");
        }
        if (userRepository.existsByEmail(user.getEmail())) {
            throw new RuntimeException("Email already exists");
        }

        //encrypt password
        user.setPassword(passwordEncoder.encode(user.getPassword()));
        return userRepository.save(user);
    }

    // Read - all users
    public List<User> getAllUsers() {
        return userRepository.findAllByOrderByCreatedAtDesc();
    }

    // Read - by ID
    public Optional<User> getUserById(Long id) {
        return userRepository.findById(id);
    }

    // Read - by username
    public Optional<User> getUserByUsername(String username) {
        return userRepository.findByUsername(username);
    }

    // Read - by email
    public Optional<User> getUserByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    // Update
    public User updateUser(Long id, User userDetails) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found"));
        
        // Update fields
        if (userDetails.getUsername() != null && !userDetails.getUsername().equals(user.getUsername())) {
            if (userRepository.existsByUsername(userDetails.getUsername())) {
                throw new RuntimeException("Username already exists");
            }
            user.setUsername(userDetails.getUsername());
        }
        
        if (userDetails.getEmail() != null && !userDetails.getEmail().equals(user.getEmail())) {
            if (userRepository.existsByEmail(userDetails.getEmail())) {
                throw new RuntimeException("Email already exists");
            }
            user.setEmail(userDetails.getEmail());
        }
        
        if (userDetails.getPassword() != null && !userDetails.getPassword().isEmpty()) {
            user.setPassword(passwordEncoder.encode(userDetails.getPassword()));
        }
        
        return userRepository.save(user);
    }

    // Delete
    public void deleteUser(Long id) {
        if (!userRepository.existsById(id)) {
            throw new RuntimeException("User not found");
        }
        userRepository.deleteById(id);
    }

}