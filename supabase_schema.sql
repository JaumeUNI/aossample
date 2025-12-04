-- Supabase Database Schema for Fitness Management System
-- Run this SQL in your Supabase SQL Editor to create all necessary tables

-- ========== EXERCISES TABLE ==========
CREATE TABLE IF NOT EXISTS exercises (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    exercise_type TEXT NOT NULL CHECK (exercise_type IN ('cardio', 'strength', 'flexibility', 'balance', 'sports')),
    difficulty TEXT NOT NULL CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
    muscle_groups JSONB NOT NULL DEFAULT '[]'::jsonb,
    duration_minutes INTEGER,
    calories_burned_per_minute INTEGER,
    equipment_needed JSONB DEFAULT '[]'::jsonb,
    instructions JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ========== USERS TABLE ==========
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    age INTEGER,
    weight_kg NUMERIC(5,2),
    height_cm NUMERIC(5,2),
    fitness_level TEXT NOT NULL DEFAULT 'beginner' CHECK (fitness_level IN ('beginner', 'intermediate', 'advanced')),
    goals JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ========== ROUTINES TABLE ==========
CREATE TABLE IF NOT EXISTS routines (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    difficulty TEXT NOT NULL CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
    target_muscle_groups JSONB NOT NULL DEFAULT '[]'::jsonb,
    estimated_duration_minutes INTEGER NOT NULL,
    exercises JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    created_by TEXT DEFAULT 'admin'
);

-- ========== SESSIONS TABLE ==========
CREATE TABLE IF NOT EXISTS sessions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    routine_id BIGINT NOT NULL REFERENCES routines(id) ON DELETE CASCADE,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    total_duration_minutes INTEGER,
    calories_burned INTEGER,
    notes TEXT,
    completed BOOLEAN DEFAULT FALSE
);

-- ========== PROGRESS TABLE ==========
CREATE TABLE IF NOT EXISTS progress (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    exercise_id BIGINT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    date TIMESTAMPTZ DEFAULT NOW(),
    weight_kg NUMERIC(5,2),
    reps INTEGER,
    sets INTEGER,
    duration_minutes INTEGER,
    personal_record BOOLEAN DEFAULT FALSE
);

-- ========== INDEXES FOR PERFORMANCE ==========
CREATE INDEX IF NOT EXISTS idx_exercises_type ON exercises(exercise_type);
CREATE INDEX IF NOT EXISTS idx_exercises_difficulty ON exercises(difficulty);
CREATE INDEX IF NOT EXISTS idx_routines_difficulty ON routines(difficulty);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_routine_id ON sessions(routine_id);
CREATE INDEX IF NOT EXISTS idx_progress_user_id ON progress(user_id);
CREATE INDEX IF NOT EXISTS idx_progress_exercise_id ON progress(exercise_id);
CREATE INDEX IF NOT EXISTS idx_progress_date ON progress(date);
