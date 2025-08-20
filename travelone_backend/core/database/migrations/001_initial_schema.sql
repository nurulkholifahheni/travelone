-- 001_initial_schema.sql
-- This migration script creates the initial tables for our application.

-- The 'uuid-ossp' extension is useful for generating Universally Unique Identifiers (UUIDs).
-- If you are not using UUIDs, you can remove this part.
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create the users table to store user authentication data.
-- This table is a core component of your authentication service.
CREATE TABLE users (
    -- 'id' is a UUID that serves as the primary key for the table.
    -- UUIDs are great for distributed systems and avoid guessable IDs.
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- 'username' stores a unique username for each user.
    -- The UNIQUE constraint ensures no two users can have the same username.
    username VARCHAR(255) UNIQUE NOT NULL,

    -- 'email' stores a unique email address for each user.
    -- This is also a common identifier for user accounts.
    email VARCHAR(255) UNIQUE NOT NULL,

    -- 'password_hash' stores the hashed password.
    -- NEVER store plain text passwords!
    -- The length of the VARCHAR should be sufficient for the hashing algorithm you use (e.g., bcrypt).
    password_hash VARCHAR(255) NOT NULL,

    -- 'created_at' automatically stores the timestamp when a user is created.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create an index on the username and email columns for faster lookups during login.
CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_users_email ON users (email);

-- Create a table for user profiles, which would be managed by your Go API service.
-- This demonstrates how a separate service might use the same database.
CREATE TABLE profiles (
    -- 'user_id' is a foreign key that links this profile to a user in the 'users' table.
    -- ON DELETE CASCADE means if a user is deleted, their profile is also deleted.
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,

    -- 'full_name' stores the user's full name.
    full_name VARCHAR(255),

    -- 'bio' stores a short biography for the user.
    bio TEXT,

    -- 'last_updated_at' stores the timestamp of the last profile update.
    last_updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
