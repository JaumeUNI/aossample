from fastapi import APIRouter, HTTPException, Query
from app.models.item import (
    Exercise, ExerciseUpdate, ExerciseType, DifficultyLevel, MuscleGroup,
    WorkoutRoutine, WorkoutRoutineUpdate, ExerciseInRoutine,
    User, UserUpdate, WorkoutSession, WorkoutSessionUpdate,
    UserProgress, UserProgressUpdate
)
from typing import List, Dict, Optional
from datetime import datetime

router = APIRouter()

# In-memory storage for all entities
exercises_storage: Dict[int, Exercise] = {}
routines_storage: Dict[int, WorkoutRoutine] = {}
users_storage: Dict[int, User] = {}
sessions_storage: Dict[int, WorkoutSession] = {}
progress_storage: Dict[int, UserProgress] = {}

# Counters for auto-incrementing IDs
exercise_counter = 1
routine_counter = 1
user_counter = 1
session_counter = 1
progress_counter = 1

# ========== EXERCISE CRUD OPERATIONS ==========

@router.post("/exercises", response_model=Exercise)
def create_exercise(exercise: Exercise):
    """Create a new exercise"""
    global exercise_counter
    exercise.id = exercise_counter
    exercises_storage[exercise_counter] = exercise
    exercise_counter += 1
    return exercise

@router.get("/exercises", response_model=List[Exercise])
def get_exercises(
    exercise_type: Optional[ExerciseType] = None,
    difficulty: Optional[DifficultyLevel] = None,
    muscle_group: Optional[MuscleGroup] = None
):
    """Get all exercises with optional filtering"""
    exercises = list(exercises_storage.values())
    
    if exercise_type:
        exercises = [e for e in exercises if e.exercise_type == exercise_type]
    if difficulty:
        exercises = [e for e in exercises if e.difficulty == difficulty]
    if muscle_group:
        exercises = [e for e in exercises if muscle_group in e.muscle_groups]
    
    return exercises

@router.get("/exercises/{exercise_id}", response_model=Exercise)
def get_exercise(exercise_id: int):
    """Get a specific exercise by ID"""
    if exercise_id not in exercises_storage:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercises_storage[exercise_id]

@router.put("/exercises/{exercise_id}", response_model=Exercise)
def update_exercise(exercise_id: int, exercise_update: ExerciseUpdate):
    """Update an exercise"""
    if exercise_id not in exercises_storage:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    existing_exercise = exercises_storage[exercise_id]
    
    # Update only provided fields
    update_data = exercise_update.model_dump(exclude_unset=True)
    updated_exercise = existing_exercise.model_copy(update=update_data)
    updated_exercise.id = exercise_id
    
    exercises_storage[exercise_id] = updated_exercise
    return updated_exercise

@router.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: int):
    """Delete an exercise"""
    if exercise_id not in exercises_storage:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    deleted_exercise = exercises_storage.pop(exercise_id)
    return {"message": f"Exercise {exercise_id} deleted successfully", "deleted_exercise": deleted_exercise}

# ========== WORKOUT ROUTINE CRUD OPERATIONS ==========

@router.post("/routines", response_model=WorkoutRoutine)
def create_routine(routine: WorkoutRoutine):
    """Create a new workout routine"""
    global routine_counter
    routine.id = routine_counter
    routine.created_at = datetime.now()
    routines_storage[routine_counter] = routine
    routine_counter += 1
    return routine

@router.get("/routines", response_model=List[WorkoutRoutine])
def get_routines(
    difficulty: Optional[DifficultyLevel] = None,
    muscle_group: Optional[MuscleGroup] = None
):
    """Get all routines with optional filtering"""
    routines = list(routines_storage.values())
    
    if difficulty:
        routines = [r for r in routines if r.difficulty == difficulty]
    if muscle_group:
        routines = [r for r in routines if muscle_group in r.target_muscle_groups]
    
    return routines

@router.get("/routines/{routine_id}", response_model=WorkoutRoutine)
def get_routine(routine_id: int):
    """Get a specific routine by ID"""
    if routine_id not in routines_storage:
        raise HTTPException(status_code=404, detail="Routine not found")
    return routines_storage[routine_id]

@router.put("/routines/{routine_id}", response_model=WorkoutRoutine)
def update_routine(routine_id: int, routine_update: WorkoutRoutineUpdate):
    """Update a routine"""
    if routine_id not in routines_storage:
        raise HTTPException(status_code=404, detail="Routine not found")
    
    existing_routine = routines_storage[routine_id]
    
    # Update only provided fields
    update_data = routine_update.model_dump(exclude_unset=True)
    updated_routine = existing_routine.model_copy(update=update_data)
    updated_routine.id = routine_id
    
    routines_storage[routine_id] = updated_routine
    return updated_routine

@router.delete("/routines/{routine_id}")
def delete_routine(routine_id: int):
    """Delete a routine"""
    if routine_id not in routines_storage:
        raise HTTPException(status_code=404, detail="Routine not found")
    
    deleted_routine = routines_storage.pop(routine_id)
    return {"message": f"Routine {routine_id} deleted successfully", "deleted_routine": deleted_routine}

# ========== USER CRUD OPERATIONS ==========

@router.post("/users", response_model=User)
def create_user(user: User):
    """Create a new user"""
    global user_counter
    user.id = user_counter
    user.created_at = datetime.now()
    users_storage[user_counter] = user
    user_counter += 1
    return user

@router.get("/users", response_model=List[User])
def get_users():
    """Get all users"""
    return list(users_storage.values())

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    """Get a specific user by ID"""
    if user_id not in users_storage:
        raise HTTPException(status_code=404, detail="User not found")
    return users_storage[user_id]

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    """Update a user"""
    if user_id not in users_storage:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_user = users_storage[user_id]
    
    # Update only provided fields
    update_data = user_update.model_dump(exclude_unset=True)
    updated_user = existing_user.model_copy(update=update_data)
    updated_user.id = user_id
    
    users_storage[user_id] = updated_user
    return updated_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Delete a user"""
    if user_id not in users_storage:
        raise HTTPException(status_code=404, detail="User not found")
    
    deleted_user = users_storage.pop(user_id)
    return {"message": f"User {user_id} deleted successfully", "deleted_user": deleted_user}

# ========== WORKOUT SESSION OPERATIONS ==========

@router.post("/sessions", response_model=WorkoutSession)
def start_workout_session(session: WorkoutSession):
    """Start a new workout session"""
    global session_counter
    
    # Validate user and routine exist
    if session.user_id not in users_storage:
        raise HTTPException(status_code=404, detail="User not found")
    if session.routine_id not in routines_storage:
        raise HTTPException(status_code=404, detail="Routine not found")
    
    session.id = session_counter
    session.started_at = datetime.now()
    sessions_storage[session_counter] = session
    session_counter += 1
    return session

@router.get("/sessions", response_model=List[WorkoutSession])
def get_sessions(user_id: Optional[int] = None):
    """Get all workout sessions, optionally filtered by user"""
    sessions = list(sessions_storage.values())
    
    if user_id:
        sessions = [s for s in sessions if s.user_id == user_id]
    
    return sessions

@router.get("/sessions/{session_id}", response_model=WorkoutSession)
def get_session(session_id: int):
    """Get a specific session by ID"""
    if session_id not in sessions_storage:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions_storage[session_id]

@router.patch("/sessions/{session_id}", response_model=WorkoutSession)
def complete_workout_session(session_id: int, session_update: WorkoutSessionUpdate):
    """Complete or update a workout session"""
    if session_id not in sessions_storage:
        raise HTTPException(status_code=404, detail="Session not found")
    
    existing_session = sessions_storage[session_id]
    
    # Update only provided fields
    update_data = session_update.model_dump(exclude_unset=True)
    updated_session = existing_session.model_copy(update=update_data)
    updated_session.id = session_id
    
    # If completing the session, set completed_at
    if session_update.completed and not existing_session.completed:
        updated_session.completed_at = datetime.now()
    
    sessions_storage[session_id] = updated_session
    return updated_session

@router.delete("/sessions/{session_id}")
def delete_session(session_id: int):
    """Delete a workout session"""
    if session_id not in sessions_storage:
        raise HTTPException(status_code=404, detail="Session not found")
    
    deleted_session = sessions_storage.pop(session_id)
    return {"message": f"Session {session_id} deleted successfully", "deleted_session": deleted_session}

# ========== USER PROGRESS OPERATIONS ==========

@router.post("/progress", response_model=UserProgress)
def record_progress(progress: UserProgress):
    """Record user progress for an exercise"""
    global progress_counter
    
    # Validate user and exercise exist
    if progress.user_id not in users_storage:
        raise HTTPException(status_code=404, detail="User not found")
    if progress.exercise_id not in exercises_storage:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    progress.id = progress_counter
    if not progress.date:
        progress.date = datetime.now()
    progress_storage[progress_counter] = progress
    progress_counter += 1
    return progress

@router.get("/progress", response_model=List[UserProgress])
def get_progress(user_id: Optional[int] = None, exercise_id: Optional[int] = None):
    """Get progress records, optionally filtered by user or exercise"""
    progress_records = list(progress_storage.values())
    
    if user_id:
        progress_records = [p for p in progress_records if p.user_id == user_id]
    if exercise_id:
        progress_records = [p for p in progress_records if p.exercise_id == exercise_id]
    
    return progress_records

@router.get("/progress/{progress_id}", response_model=UserProgress)
def get_progress_record(progress_id: int):
    """Get a specific progress record by ID"""
    if progress_id not in progress_storage:
        raise HTTPException(status_code=404, detail="Progress record not found")
    return progress_storage[progress_id]

@router.put("/progress/{progress_id}", response_model=UserProgress)
def update_progress(progress_id: int, progress_update: UserProgressUpdate):
    """Update a progress record"""
    if progress_id not in progress_storage:
        raise HTTPException(status_code=404, detail="Progress record not found")
    
    existing_progress = progress_storage[progress_id]
    
    # Update only provided fields
    update_data = progress_update.model_dump(exclude_unset=True)
    updated_progress = existing_progress.model_copy(update=update_data)
    updated_progress.id = progress_id
    
    progress_storage[progress_id] = updated_progress
    return updated_progress

@router.delete("/progress/{progress_id}")
def delete_progress(progress_id: int):
    """Delete a progress record"""
    if progress_id not in progress_storage:
        raise HTTPException(status_code=404, detail="Progress record not found")
    
    deleted_progress = progress_storage.pop(progress_id)
    return {"message": f"Progress record {progress_id} deleted successfully", "deleted_progress": deleted_progress}

# ========== ANALYTICS AND STATS ==========

@router.get("/stats/user/{user_id}")
def get_user_stats(user_id: int):
    """Get statistics for a specific user"""
    if user_id not in users_storage:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's sessions
    user_sessions = [s for s in sessions_storage.values() if s.user_id == user_id]
    completed_sessions = [s for s in user_sessions if s.completed]
    
    # Get user's progress
    user_progress = [p for p in progress_storage.values() if p.user_id == user_id]
    personal_records = [p for p in user_progress if p.personal_record]
    
    stats = {
        "user_id": user_id,
        "total_sessions": len(user_sessions),
        "completed_sessions": len(completed_sessions),
        "total_workout_time_minutes": sum(s.total_duration_minutes or 0 for s in completed_sessions),
        "total_calories_burned": sum(s.calories_burned or 0 for s in completed_sessions),
        "progress_records": len(user_progress),
        "personal_records": len(personal_records),
        "completion_rate": len(completed_sessions) / len(user_sessions) if user_sessions else 0
    }
    
    return stats

@router.get("/stats/exercise/{exercise_id}")
def get_exercise_stats(exercise_id: int):
    """Get statistics for a specific exercise"""
    if exercise_id not in exercises_storage:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    exercise_progress = [p for p in progress_storage.values() if p.exercise_id == exercise_id]
    personal_records = [p for p in exercise_progress if p.personal_record]
    
    stats = {
        "exercise_id": exercise_id,
        "exercise_name": exercises_storage[exercise_id].name,
        "total_attempts": len(exercise_progress),
        "unique_users": len(set(p.user_id for p in exercise_progress)),
        "personal_records": len(personal_records),
        "average_weight": sum(p.weight_kg or 0 for p in exercise_progress) / len(exercise_progress) if exercise_progress else 0,
        "average_reps": sum(p.reps or 0 for p in exercise_progress) / len(exercise_progress) if exercise_progress else 0
    }
    
    return stats
