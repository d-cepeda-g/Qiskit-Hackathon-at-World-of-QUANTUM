-- Quantum Hackathon Database Initialization
-- This file is automatically executed when the MySQL container starts

USE quantum_hackathon;

-- Set the timezone to UTC for consistent timestamp handling
SET time_zone = '+00:00';

-- Ensure we're using UTF8MB4 for full Unicode support
ALTER DATABASE quantum_hackathon CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create indexes for better performance (will be created by migrations, but good to have as backup)
-- These will be created automatically by Fluent migrations, but included here for reference

-- Example data for testing (optional)
-- INSERT INTO users (id, username, email, full_name, experience_level, created_at, updated_at) 
-- VALUES 
--   (UUID(), 'alice_quantum', 'alice@example.com', 'Alice Johnson', 'Advanced', NOW(), NOW()),
--   (UUID(), 'bob_circuits', 'bob@example.com', 'Bob Smith', 'Beginner', NOW(), NOW());

-- Log initialization
SELECT 'Quantum Hackathon Database Initialized Successfully' AS status;