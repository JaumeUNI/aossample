from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime

client = TestClient(app)

# ========== EXERCISE CRUD TESTS ==========

def test_create_exercise():
    """Test creating a new exercise"""
    response = client.post("/exercises", json={
        "name": "Push-ups",
        "description": "Classic bodyweight exercise for chest and arms",
        "exercise_type": "strength",
        "difficulty": "beginner",
        "muscle_groups": ["chest", "arms"],
        "duration_minutes": 5,
        "calories_burned_per_minute": 8,
        "equipment_needed": [],
        "instructions": ["Start in plank position", "Lower body to ground", "Push back up"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Push-ups"
    assert data["exercise_type"] == "strength"
    assert data["id"] == 1

def test_get_exercises():
    """Test getting all exercises"""
    response = client.get("/exercises")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Push-ups"

def test_get_exercises_with_filters():
    """Test getting exercises with filters"""
    # Create another exercise
    client.post("/exercises", json={
        "name": "Running",
        "description": "Cardio exercise",
        "exercise_type": "cardio",
        "difficulty": "beginner",
        "muscle_groups": ["legs"],
        "duration_minutes": 30,
        "calories_burned_per_minute": 12
    })
    
    # Filter by exercise type
    response = client.get("/exercises?exercise_type=cardio")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["exercise_type"] == "cardio"

def test_get_exercise_by_id():
    """Test getting a specific exercise by ID"""
    response = client.get("/exercises/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Push-ups"

def test_update_exercise():
    """Test updating an exercise"""
    response = client.put("/exercises/1", json={
        "name": "Modified Push-ups",
        "description": "Updated description",
        "exercise_type": "strength",
        "difficulty": "intermediate",
        "muscle_groups": ["chest", "arms", "core"],
        "duration_minutes": 7
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Modified Push-ups"
    assert data["difficulty"] == "intermediate"
    assert "core" in data["muscle_groups"]

def test_delete_exercise():
    """Test deleting an exercise"""
    response = client.delete("/exercises/1")
    assert response.status_code == 200
    data = response.json()
    assert "deleted successfully" in data["message"]

# ========== USER CRUD TESTS ==========

def test_create_user():
    """Test creating a new user"""
    response = client.post("/users", json={
        "username": "john_doe",
        "email": "john@example.com",
        "age": 25,
        "weight_kg": 70.0,
        "height_cm": 175.0,
        "fitness_level": "beginner",
        "goals": ["lose_weight", "build_muscle"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "john_doe"
    assert data["fitness_level"] == "beginner"
    assert data["id"] == 1

def test_get_users():
    """Test getting all users"""
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["username"] == "john_doe"

def test_get_user_by_id():
    """Test getting a specific user by ID"""
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "john_doe"

def test_update_user():
    """Test updating a user"""
    response = client.put("/users/1", json={
        "fitness_level": "intermediate",
        "weight_kg": 68.0,
        "goals": ["build_muscle", "improve_endurance"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["fitness_level"] == "intermediate"
    assert data["weight_kg"] == 68.0

def test_delete_user():
    """Test deleting a user"""
    response = client.delete("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert "deleted successfully" in data["message"]

# ========== WORKOUT ROUTINE CRUD TESTS ==========

def test_create_routine():
    """Test creating a workout routine"""
    # First create some exercises
    client.post("/exercises", json={
        "name": "Squats",
        "description": "Leg exercise",
        "exercise_type": "strength",
        "difficulty": "beginner",
        "muscle_groups": ["legs"]
    })
    client.post("/exercises", json={
        "name": "Planks",
        "description": "Core exercise",
        "exercise_type": "strength",
        "difficulty": "beginner",
        "muscle_groups": ["core"]
    })
    
    response = client.post("/routines", json={
        "name": "Beginner Full Body",
        "description": "A complete workout for beginners",
        "difficulty": "beginner",
        "target_muscle_groups": ["legs", "core"],
        "estimated_duration_minutes": 30,
        "exercises": [
            {"exercise_id": 1, "sets": 3, "reps": 15, "rest_seconds": 60},
            {"exercise_id": 2, "duration_minutes": 1, "rest_seconds": 30}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Beginner Full Body"
    assert data["id"] == 1
    assert len(data["exercises"]) == 2

def test_get_routines():
    """Test getting all routines"""
    response = client.get("/routines")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Beginner Full Body"

def test_get_routine_by_id():
    """Test getting a specific routine by ID"""
    response = client.get("/routines/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Beginner Full Body"

def test_update_routine():
    """Test updating a routine"""
    response = client.put("/routines/1", json={
        "name": "Advanced Full Body",
        "difficulty": "advanced",
        "estimated_duration_minutes": 45
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Advanced Full Body"
    assert data["difficulty"] == "advanced"

def test_delete_routine():
    """Test deleting a routine"""
    response = client.delete("/routines/1")
    assert response.status_code == 200
    data = response.json()
    assert "deleted successfully" in data["message"]

# ========== WORKOUT SESSION TESTS ==========

def test_start_workout_session():
    """Test starting a workout session"""
    # Create user and routine first
    user_response = client.post("/users", json={
        "username": "test_user",
        "email": "test@example.com",
        "fitness_level": "beginner"
    })
    user_id = user_response.json()["id"]
    
    routine_response = client.post("/routines", json={
        "name": "Test Routine",
        "description": "Test routine",
        "difficulty": "beginner",
        "target_muscle_groups": ["legs"],
        "estimated_duration_minutes": 20
    })
    routine_id = routine_response.json()["id"]
    
    response = client.post("/sessions", json={
        "user_id": user_id,
        "routine_id": routine_id,
        "started_at": datetime.now().isoformat()
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["routine_id"] == routine_id
    assert data["id"] == 1

def test_complete_workout_session():
    """Test completing a workout session"""
    response = client.patch("/sessions/1", json={
        "completed": True,
        "total_duration_minutes": 25,
        "calories_burned": 200,
        "notes": "Great workout!"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] == True
    assert data["total_duration_minutes"] == 25
    assert data["calories_burned"] == 200

def test_get_sessions():
    """Test getting all sessions"""
    response = client.get("/sessions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

# ========== USER PROGRESS TESTS ==========

def test_record_progress():
    """Test recording user progress"""
    # Create user and exercise first
    user_response = client.post("/users", json={
        "username": "progress_user",
        "email": "progress@example.com",
        "fitness_level": "beginner"
    })
    user_id = user_response.json()["id"]
    
    exercise_response = client.post("/exercises", json={
        "name": "Bench Press",
        "description": "Chest exercise",
        "exercise_type": "strength",
        "difficulty": "intermediate",
        "muscle_groups": ["chest"]
    })
    exercise_id = exercise_response.json()["id"]
    
    response = client.post("/progress", json={
        "user_id": user_id,
        "exercise_id": exercise_id,
        "weight_kg": 50.0,
        "reps": 10,
        "sets": 3,
        "personal_record": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["exercise_id"] == exercise_id
    assert data["weight_kg"] == 50.0
    assert data["personal_record"] == True

def test_get_progress():
    """Test getting progress records"""
    response = client.get("/progress")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

# ========== STATISTICS TESTS ==========

def test_get_user_stats():
    """Test getting user statistics"""
    user_response = client.post("/users", json={
        "username": "stats_user",
        "email": "stats@example.com",
        "fitness_level": "intermediate"
    })
    user_id = user_response.json()["id"]
    
    response = client.get(f"/stats/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert "total_sessions" in data
    assert "completed_sessions" in data
    assert "completion_rate" in data

def test_get_exercise_stats():
    """Test getting exercise statistics"""
    exercise_response = client.post("/exercises", json={
        "name": "Stats Exercise",
        "description": "Exercise for stats testing",
        "exercise_type": "strength",
        "difficulty": "beginner",
        "muscle_groups": ["arms"]
    })
    exercise_id = exercise_response.json()["id"]
    
    response = client.get(f"/stats/exercise/{exercise_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["exercise_id"] == exercise_id
    assert "total_attempts" in data
    assert "unique_users" in data

# ========== ERROR HANDLING TESTS ==========

def test_get_nonexistent_exercise():
    """Test getting a non-existent exercise"""
    response = client.get("/exercises/999")
    assert response.status_code == 404
    assert "Exercise not found" in response.json()["detail"]

def test_get_nonexistent_user():
    """Test getting a non-existent user"""
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

def test_get_nonexistent_routine():
    """Test getting a non-existent routine"""
    response = client.get("/routines/999")
    assert response.status_code == 404
    assert "Routine not found" in response.json()["detail"]

def test_create_session_invalid_user():
    """Test creating session with invalid user"""
    response = client.post("/sessions", json={
        "user_id": 999,
        "routine_id": 1,
        "started_at": datetime.now().isoformat()
    })
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

def test_create_session_invalid_routine():
    """Test creating session with invalid routine"""
    user_response = client.post("/users", json={
        "username": "invalid_session_user",
        "email": "invalid@example.com",
        "fitness_level": "beginner"
    })
    user_id = user_response.json()["id"]
    
    response = client.post("/sessions", json={
        "user_id": user_id,
        "routine_id": 999,
        "started_at": datetime.now().isoformat()
    })
    assert response.status_code == 404
    assert "Routine not found" in response.json()["detail"]

def test_record_progress_invalid_user():
    """Test recording progress with invalid user"""
    exercise_response = client.post("/exercises", json={
        "name": "Invalid Progress Exercise",
        "description": "Exercise for invalid progress test",
        "exercise_type": "strength",
        "difficulty": "beginner",
        "muscle_groups": ["legs"]
    })
    exercise_id = exercise_response.json()["id"]
    
    response = client.post("/progress", json={
        "user_id": 999,
        "exercise_id": exercise_id,
        "weight_kg": 30.0,
        "reps": 8
    })
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

def test_record_progress_invalid_exercise():
    """Test recording progress with invalid exercise"""
    user_response = client.post("/users", json={
        "username": "invalid_progress_user",
        "email": "invalid_progress@example.com",
        "fitness_level": "beginner"
    })
    user_id = user_response.json()["id"]
    
    response = client.post("/progress", json={
        "user_id": user_id,
        "exercise_id": 999,
        "weight_kg": 30.0,
        "reps": 8
    })
    assert response.status_code == 404
    assert "Exercise not found" in response.json()["detail"]

