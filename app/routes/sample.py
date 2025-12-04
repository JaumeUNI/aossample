from fastapi import APIRouter, HTTPException, Query
from app.models.item import (
    Exercise, ExerciseUpdate, ExerciseType, DifficultyLevel, MuscleGroup,
    WorkoutRoutine, WorkoutRoutineUpdate, ExerciseInRoutine,
    User, UserUpdate, WorkoutSession, WorkoutSessionUpdate,
    UserProgress, UserProgressUpdate
)
from app.db import supabase
from typing import List, Dict, Optional
from datetime import datetime

router = APIRouter()

# ========== EXERCISE CRUD OPERATIONS ==========

@router.post("/exercises", response_model=Exercise)
def create_exercise(exercise: Exercise):
    """Create a new exercise"""
    # Prepare data for Supabase
    exercise_data = {
        "name": exercise.name,
        "description": exercise.description,
        "exercise_type": exercise.exercise_type.value,
        "difficulty": exercise.difficulty.value,
        "muscle_groups": [mg.value for mg in exercise.muscle_groups],
        "duration_minutes": exercise.duration_minutes,
        "calories_burned_per_minute": exercise.calories_burned_per_minute,
        "equipment_needed": exercise.equipment_needed,
        "instructions": exercise.instructions
    }
    
    try:
        result = supabase.table("exercises").insert(exercise_data).execute()
        if result.data:
            created = result.data[0]
            # Convert back to Exercise model
            exercise.id = created["id"]
            exercise.exercise_type = ExerciseType(created["exercise_type"])
            exercise.difficulty = DifficultyLevel(created["difficulty"])
            exercise.muscle_groups = [MuscleGroup(mg) for mg in created["muscle_groups"]]
            return exercise
        raise HTTPException(status_code=500, detail="Failed to create exercise")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating exercise: {str(e)}")

@router.get("/exercises", response_model=List[Exercise])
def get_exercises(
    exercise_type: Optional[ExerciseType] = None,
    difficulty: Optional[DifficultyLevel] = None,
    muscle_group: Optional[MuscleGroup] = None
):
    """Get all exercises with optional filtering"""
    try:
        query = supabase.table("exercises").select("*")
        
        if exercise_type:
            query = query.eq("exercise_type", exercise_type.value)
        if difficulty:
            query = query.eq("difficulty", difficulty.value)
        
        result = query.execute()
        
        exercises = []
        for row in result.data:
            # Filter by muscle_group in Python if specified
            if muscle_group:
                muscle_groups = row.get("muscle_groups", [])
                if muscle_group.value not in muscle_groups:
                    continue
            
            exercise = Exercise(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                exercise_type=ExerciseType(row["exercise_type"]),
                difficulty=DifficultyLevel(row["difficulty"]),
                muscle_groups=[MuscleGroup(mg) for mg in row["muscle_groups"]],
                duration_minutes=row.get("duration_minutes"),
                calories_burned_per_minute=row.get("calories_burned_per_minute"),
                equipment_needed=row.get("equipment_needed", []),
                instructions=row.get("instructions", [])
            )
            exercises.append(exercise)
        
        return exercises
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching exercises: {str(e)}")

@router.get("/exercises/{exercise_id}", response_model=Exercise)
def get_exercise(exercise_id: int):
    """Get a specific exercise by ID"""
    try:
        result = supabase.table("exercises").select("*").eq("id", exercise_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Exercise not found")
        
        row = result.data[0]
        return Exercise(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            exercise_type=ExerciseType(row["exercise_type"]),
            difficulty=DifficultyLevel(row["difficulty"]),
            muscle_groups=[MuscleGroup(mg) for mg in row["muscle_groups"]],
            duration_minutes=row.get("duration_minutes"),
            calories_burned_per_minute=row.get("calories_burned_per_minute"),
            equipment_needed=row.get("equipment_needed", []),
            instructions=row.get("instructions", [])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching exercise: {str(e)}")

@router.put("/exercises/{exercise_id}", response_model=Exercise)
def update_exercise(exercise_id: int, exercise_update: ExerciseUpdate):
    """Update an exercise"""
    try:
        # Get existing exercise
        result = supabase.table("exercises").select("*").eq("id", exercise_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Exercise not found")
        
        existing = result.data[0]
        
        # Prepare update data
        update_data = exercise_update.model_dump(exclude_unset=True)
        
        # Convert enums to values if present
        if "exercise_type" in update_data and update_data["exercise_type"]:
            update_data["exercise_type"] = update_data["exercise_type"].value
        if "difficulty" in update_data and update_data["difficulty"]:
            update_data["difficulty"] = update_data["difficulty"].value
        if "muscle_groups" in update_data and update_data["muscle_groups"]:
            update_data["muscle_groups"] = [mg.value for mg in update_data["muscle_groups"]]
        
        # Update in Supabase
        result = supabase.table("exercises").update(update_data).eq("id", exercise_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to update exercise")
        
        row = result.data[0]
        return Exercise(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            exercise_type=ExerciseType(row["exercise_type"]),
            difficulty=DifficultyLevel(row["difficulty"]),
            muscle_groups=[MuscleGroup(mg) for mg in row["muscle_groups"]],
            duration_minutes=row.get("duration_minutes"),
            calories_burned_per_minute=row.get("calories_burned_per_minute"),
            equipment_needed=row.get("equipment_needed", []),
            instructions=row.get("instructions", [])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating exercise: {str(e)}")

@router.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: int):
    """Delete an exercise"""
    try:
        # Get exercise before deleting
        result = supabase.table("exercises").select("*").eq("id", exercise_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Exercise not found")
        
        deleted_data = result.data[0]
        
        # Delete from Supabase
        supabase.table("exercises").delete().eq("id", exercise_id).execute()
        
        return {"message": f"Exercise {exercise_id} deleted successfully", "deleted_exercise": deleted_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting exercise: {str(e)}")

# ========== WORKOUT ROUTINE CRUD OPERATIONS ==========

@router.post("/routines", response_model=WorkoutRoutine)
def create_routine(routine: WorkoutRoutine):
    """Create a new workout routine"""
    routine_data = {
        "name": routine.name,
        "description": routine.description,
        "difficulty": routine.difficulty.value,
        "target_muscle_groups": [mg.value for mg in routine.target_muscle_groups],
        "estimated_duration_minutes": routine.estimated_duration_minutes,
        "exercises": [ex.model_dump() for ex in routine.exercises],
        "created_at": datetime.now().isoformat(),
        "created_by": routine.created_by or "admin"
    }
    
    try:
        result = supabase.table("routines").insert(routine_data).execute()
        if result.data:
            created = result.data[0]
            routine.id = created["id"]
            routine.created_at = datetime.fromisoformat(created["created_at"].replace("Z", "+00:00"))
            return routine
        raise HTTPException(status_code=500, detail="Failed to create routine")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating routine: {str(e)}")

@router.get("/routines", response_model=List[WorkoutRoutine])
def get_routines(
    difficulty: Optional[DifficultyLevel] = None,
    muscle_group: Optional[MuscleGroup] = None
):
    """Get all routines with optional filtering"""
    try:
        query = supabase.table("routines").select("*")
        
        if difficulty:
            query = query.eq("difficulty", difficulty.value)
        
        result = query.execute()
        
        routines = []
        for row in result.data:
            # Filter by muscle_group in Python if specified
            if muscle_group:
                target_muscle_groups = row.get("target_muscle_groups", [])
                if muscle_group.value not in target_muscle_groups:
                    continue
            
            routine = WorkoutRoutine(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                difficulty=DifficultyLevel(row["difficulty"]),
                target_muscle_groups=[MuscleGroup(mg) for mg in row["target_muscle_groups"]],
                estimated_duration_minutes=row["estimated_duration_minutes"],
                exercises=[ExerciseInRoutine(**ex) for ex in row.get("exercises", [])],
                created_at=datetime.fromisoformat(row["created_at"].replace("Z", "+00:00")) if row.get("created_at") else None,
                created_by=row.get("created_by", "admin")
            )
            routines.append(routine)
        
        return routines
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching routines: {str(e)}")

@router.get("/routines/{routine_id}", response_model=WorkoutRoutine)
def get_routine(routine_id: int):
    """Get a specific routine by ID"""
    try:
        result = supabase.table("routines").select("*").eq("id", routine_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Routine not found")
        
        row = result.data[0]
        return WorkoutRoutine(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            difficulty=DifficultyLevel(row["difficulty"]),
            target_muscle_groups=[MuscleGroup(mg) for mg in row["target_muscle_groups"]],
            estimated_duration_minutes=row["estimated_duration_minutes"],
            exercises=[ExerciseInRoutine(**ex) for ex in row.get("exercises", [])],
            created_at=datetime.fromisoformat(row["created_at"].replace("Z", "+00:00")) if row.get("created_at") else None,
            created_by=row.get("created_by", "admin")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching routine: {str(e)}")

@router.put("/routines/{routine_id}", response_model=WorkoutRoutine)
def update_routine(routine_id: int, routine_update: WorkoutRoutineUpdate):
    """Update a routine"""
    try:
        result = supabase.table("routines").select("*").eq("id", routine_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Routine not found")
        
        update_data = routine_update.model_dump(exclude_unset=True)
        
        if "difficulty" in update_data and update_data["difficulty"]:
            update_data["difficulty"] = update_data["difficulty"].value
        if "target_muscle_groups" in update_data and update_data["target_muscle_groups"]:
            update_data["target_muscle_groups"] = [mg.value for mg in update_data["target_muscle_groups"]]
        if "exercises" in update_data and update_data["exercises"]:
            update_data["exercises"] = [ex.model_dump() if hasattr(ex, "model_dump") else ex for ex in update_data["exercises"]]
        
        result = supabase.table("routines").update(update_data).eq("id", routine_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to update routine")
        
        row = result.data[0]
        return WorkoutRoutine(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            difficulty=DifficultyLevel(row["difficulty"]),
            target_muscle_groups=[MuscleGroup(mg) for mg in row["target_muscle_groups"]],
            estimated_duration_minutes=row["estimated_duration_minutes"],
            exercises=[ExerciseInRoutine(**ex) for ex in row.get("exercises", [])],
            created_at=datetime.fromisoformat(row["created_at"].replace("Z", "+00:00")) if row.get("created_at") else None,
            created_by=row.get("created_by", "admin")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating routine: {str(e)}")

@router.delete("/routines/{routine_id}")
def delete_routine(routine_id: int):
    """Delete a routine"""
    try:
        result = supabase.table("routines").select("*").eq("id", routine_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Routine not found")
        
        deleted_data = result.data[0]
        supabase.table("routines").delete().eq("id", routine_id).execute()
        
        return {"message": f"Routine {routine_id} deleted successfully", "deleted_routine": deleted_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting routine: {str(e)}")

# ========== USER CRUD OPERATIONS ==========

@router.post("/users", response_model=User)
def create_user(user: User):
    """Create a new user"""
    user_data = {
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "weight_kg": user.weight_kg,
        "height_cm": user.height_cm,
        "fitness_level": user.fitness_level.value,
        "goals": user.goals,
        "created_at": datetime.now().isoformat()
    }
    
    try:
        result = supabase.table("users").insert(user_data).execute()
        if result.data:
            created = result.data[0]
            user.id = created["id"]
            user.fitness_level = DifficultyLevel(created["fitness_level"])
            user.created_at = datetime.fromisoformat(created["created_at"].replace("Z", "+00:00"))
            return user
        raise HTTPException(status_code=500, detail="Failed to create user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@router.get("/users", response_model=List[User])
def get_users():
    """Get all users"""
    try:
        result = supabase.table("users").select("*").execute()
        
        users = []
        for row in result.data:
            user = User(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                age=row.get("age"),
                weight_kg=row.get("weight_kg"),
                height_cm=row.get("height_cm"),
                fitness_level=DifficultyLevel(row["fitness_level"]),
                goals=row.get("goals", []),
                created_at=datetime.fromisoformat(row["created_at"].replace("Z", "+00:00")) if row.get("created_at") else None
            )
            users.append(user)
        
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    """Get a specific user by ID"""
    try:
        result = supabase.table("users").select("*").eq("id", user_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        row = result.data[0]
        return User(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            age=row.get("age"),
            weight_kg=row.get("weight_kg"),
            height_cm=row.get("height_cm"),
            fitness_level=DifficultyLevel(row["fitness_level"]),
            goals=row.get("goals", []),
            created_at=datetime.fromisoformat(row["created_at"].replace("Z", "+00:00")) if row.get("created_at") else None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    """Update a user"""
    try:
        result = supabase.table("users").select("*").eq("id", user_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        update_data = user_update.model_dump(exclude_unset=True)
        
        if "fitness_level" in update_data and update_data["fitness_level"]:
            update_data["fitness_level"] = update_data["fitness_level"].value
        
        result = supabase.table("users").update(update_data).eq("id", user_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to update user")
        
        row = result.data[0]
        return User(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            age=row.get("age"),
            weight_kg=row.get("weight_kg"),
            height_cm=row.get("height_cm"),
            fitness_level=DifficultyLevel(row["fitness_level"]),
            goals=row.get("goals", []),
            created_at=datetime.fromisoformat(row["created_at"].replace("Z", "+00:00")) if row.get("created_at") else None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Delete a user"""
    try:
        result = supabase.table("users").select("*").eq("id", user_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        deleted_data = result.data[0]
        supabase.table("users").delete().eq("id", user_id).execute()
        
        return {"message": f"User {user_id} deleted successfully", "deleted_user": deleted_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")

# ========== WORKOUT SESSION OPERATIONS ==========

@router.post("/sessions", response_model=WorkoutSession)
def start_workout_session(session: WorkoutSession):
    """Start a new workout session"""
    # Validate user and routine exist
    user_result = supabase.table("users").select("id").eq("id", session.user_id).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    routine_result = supabase.table("routines").select("id").eq("id", session.routine_id).execute()
    if not routine_result.data:
        raise HTTPException(status_code=404, detail="Routine not found")
    
    session_data = {
        "user_id": session.user_id,
        "routine_id": session.routine_id,
        "started_at": session.started_at.isoformat() if isinstance(session.started_at, datetime) else session.started_at,
        "completed": session.completed,
        "completed_at": session.completed_at.isoformat() if session.completed_at and isinstance(session.completed_at, datetime) else session.completed_at,
        "total_duration_minutes": session.total_duration_minutes,
        "calories_burned": session.calories_burned,
        "notes": session.notes
    }
    
    try:
        result = supabase.table("sessions").insert(session_data).execute()
        if result.data:
            created = result.data[0]
            session.id = created["id"]
            session.started_at = datetime.fromisoformat(created["started_at"].replace("Z", "+00:00"))
            if created.get("completed_at"):
                session.completed_at = datetime.fromisoformat(created["completed_at"].replace("Z", "+00:00"))
            return session
        raise HTTPException(status_code=500, detail="Failed to create session")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")

@router.get("/sessions", response_model=List[WorkoutSession])
def get_sessions(user_id: Optional[int] = None):
    """Get all workout sessions, optionally filtered by user"""
    try:
        query = supabase.table("sessions").select("*")
        
        if user_id:
            query = query.eq("user_id", user_id)
        
        result = query.execute()
        
        sessions = []
        for row in result.data:
            session = WorkoutSession(
                id=row["id"],
                user_id=row["user_id"],
                routine_id=row["routine_id"],
                started_at=datetime.fromisoformat(row["started_at"].replace("Z", "+00:00")),
                completed_at=datetime.fromisoformat(row["completed_at"].replace("Z", "+00:00")) if row.get("completed_at") else None,
                total_duration_minutes=row.get("total_duration_minutes"),
                calories_burned=row.get("calories_burned"),
                notes=row.get("notes"),
                completed=row.get("completed", False)
            )
            sessions.append(session)
        
        return sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sessions: {str(e)}")

@router.get("/sessions/{session_id}", response_model=WorkoutSession)
def get_session(session_id: int):
    """Get a specific session by ID"""
    try:
        result = supabase.table("sessions").select("*").eq("id", session_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        row = result.data[0]
        return WorkoutSession(
            id=row["id"],
            user_id=row["user_id"],
            routine_id=row["routine_id"],
            started_at=datetime.fromisoformat(row["started_at"].replace("Z", "+00:00")),
            completed_at=datetime.fromisoformat(row["completed_at"].replace("Z", "+00:00")) if row.get("completed_at") else None,
            total_duration_minutes=row.get("total_duration_minutes"),
            calories_burned=row.get("calories_burned"),
            notes=row.get("notes"),
            completed=row.get("completed", False)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching session: {str(e)}")

@router.patch("/sessions/{session_id}", response_model=WorkoutSession)
def complete_workout_session(session_id: int, session_update: WorkoutSessionUpdate):
    """Complete or update a workout session"""
    try:
        result = supabase.table("sessions").select("*").eq("id", session_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        existing = result.data[0]
        update_data = session_update.model_dump(exclude_unset=True)
        
        # If completing the session, set completed_at
        if session_update.completed and not existing.get("completed"):
            update_data["completed_at"] = datetime.now().isoformat()
        
        if "completed_at" in update_data and isinstance(update_data["completed_at"], datetime):
            update_data["completed_at"] = update_data["completed_at"].isoformat()
        
        result = supabase.table("sessions").update(update_data).eq("id", session_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to update session")
        
        row = result.data[0]
        return WorkoutSession(
            id=row["id"],
            user_id=row["user_id"],
            routine_id=row["routine_id"],
            started_at=datetime.fromisoformat(row["started_at"].replace("Z", "+00:00")),
            completed_at=datetime.fromisoformat(row["completed_at"].replace("Z", "+00:00")) if row.get("completed_at") else None,
            total_duration_minutes=row.get("total_duration_minutes"),
            calories_burned=row.get("calories_burned"),
            notes=row.get("notes"),
            completed=row.get("completed", False)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating session: {str(e)}")

@router.delete("/sessions/{session_id}")
def delete_session(session_id: int):
    """Delete a workout session"""
    try:
        result = supabase.table("sessions").select("*").eq("id", session_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        deleted_data = result.data[0]
        supabase.table("sessions").delete().eq("id", session_id).execute()
        
        return {"message": f"Session {session_id} deleted successfully", "deleted_session": deleted_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")

# ========== USER PROGRESS OPERATIONS ==========

@router.post("/progress", response_model=UserProgress)
def record_progress(progress: UserProgress):
    """Record user progress for an exercise"""
    # Validate user and exercise exist
    user_result = supabase.table("users").select("id").eq("id", progress.user_id).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    exercise_result = supabase.table("exercises").select("id").eq("id", progress.exercise_id).execute()
    if not exercise_result.data:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    progress_data = {
        "user_id": progress.user_id,
        "exercise_id": progress.exercise_id,
        "date": (progress.date or datetime.now()).isoformat() if isinstance(progress.date or datetime.now(), datetime) else (progress.date or datetime.now()),
        "weight_kg": progress.weight_kg,
        "reps": progress.reps,
        "sets": progress.sets,
        "duration_minutes": progress.duration_minutes,
        "personal_record": progress.personal_record
    }
    
    try:
        result = supabase.table("progress").insert(progress_data).execute()
        if result.data:
            created = result.data[0]
            progress.id = created["id"]
            if created.get("date"):
                progress.date = datetime.fromisoformat(created["date"].replace("Z", "+00:00"))
            return progress
        raise HTTPException(status_code=500, detail="Failed to create progress record")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating progress record: {str(e)}")

@router.get("/progress", response_model=List[UserProgress])
def get_progress(user_id: Optional[int] = None, exercise_id: Optional[int] = None):
    """Get progress records, optionally filtered by user or exercise"""
    try:
        query = supabase.table("progress").select("*")
        
        if user_id:
            query = query.eq("user_id", user_id)
        if exercise_id:
            query = query.eq("exercise_id", exercise_id)
        
        result = query.execute()
        
        progress_records = []
        for row in result.data:
            progress = UserProgress(
                id=row["id"],
                user_id=row["user_id"],
                exercise_id=row["exercise_id"],
                date=datetime.fromisoformat(row["date"].replace("Z", "+00:00")) if row.get("date") else None,
                weight_kg=row.get("weight_kg"),
                reps=row.get("reps"),
                sets=row.get("sets"),
                duration_minutes=row.get("duration_minutes"),
                personal_record=row.get("personal_record", False)
            )
            progress_records.append(progress)
        
        return progress_records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching progress: {str(e)}")

@router.get("/progress/{progress_id}", response_model=UserProgress)
def get_progress_record(progress_id: int):
    """Get a specific progress record by ID"""
    try:
        result = supabase.table("progress").select("*").eq("id", progress_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Progress record not found")
        
        row = result.data[0]
        return UserProgress(
            id=row["id"],
            user_id=row["user_id"],
            exercise_id=row["exercise_id"],
            date=datetime.fromisoformat(row["date"].replace("Z", "+00:00")) if row.get("date") else None,
            weight_kg=row.get("weight_kg"),
            reps=row.get("reps"),
            sets=row.get("sets"),
            duration_minutes=row.get("duration_minutes"),
            personal_record=row.get("personal_record", False)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching progress record: {str(e)}")

@router.put("/progress/{progress_id}", response_model=UserProgress)
def update_progress(progress_id: int, progress_update: UserProgressUpdate):
    """Update a progress record"""
    try:
        result = supabase.table("progress").select("*").eq("id", progress_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Progress record not found")
        
        update_data = progress_update.model_dump(exclude_unset=True)
        
        result = supabase.table("progress").update(update_data).eq("id", progress_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to update progress record")
        
        row = result.data[0]
        return UserProgress(
            id=row["id"],
            user_id=row["user_id"],
            exercise_id=row["exercise_id"],
            date=datetime.fromisoformat(row["date"].replace("Z", "+00:00")) if row.get("date") else None,
            weight_kg=row.get("weight_kg"),
            reps=row.get("reps"),
            sets=row.get("sets"),
            duration_minutes=row.get("duration_minutes"),
            personal_record=row.get("personal_record", False)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating progress record: {str(e)}")

@router.delete("/progress/{progress_id}")
def delete_progress(progress_id: int):
    """Delete a progress record"""
    try:
        result = supabase.table("progress").select("*").eq("id", progress_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Progress record not found")
        
        deleted_data = result.data[0]
        supabase.table("progress").delete().eq("id", progress_id).execute()
        
        return {"message": f"Progress record {progress_id} deleted successfully", "deleted_progress": deleted_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting progress record: {str(e)}")

# ========== ANALYTICS AND STATS ==========

@router.get("/stats/user/{user_id}")
def get_user_stats(user_id: int):
    """Get statistics for a specific user"""
    try:
        # Check if user exists
        user_result = supabase.table("users").select("id").eq("id", user_id).execute()
        if not user_result.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user's sessions
        sessions_result = supabase.table("sessions").select("*").eq("user_id", user_id).execute()
        user_sessions = sessions_result.data
        completed_sessions = [s for s in user_sessions if s.get("completed", False)]
        
        # Get user's progress
        progress_result = supabase.table("progress").select("*").eq("user_id", user_id).execute()
        user_progress = progress_result.data
        personal_records = [p for p in user_progress if p.get("personal_record", False)]
        
        stats = {
            "user_id": user_id,
            "total_sessions": len(user_sessions),
            "completed_sessions": len(completed_sessions),
            "total_workout_time_minutes": sum(s.get("total_duration_minutes") or 0 for s in completed_sessions),
            "total_calories_burned": sum(s.get("calories_burned") or 0 for s in completed_sessions),
            "progress_records": len(user_progress),
            "personal_records": len(personal_records),
            "completion_rate": len(completed_sessions) / len(user_sessions) if user_sessions else 0
        }
        
        return stats
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user stats: {str(e)}")

@router.get("/stats/exercise/{exercise_id}")
def get_exercise_stats(exercise_id: int):
    """Get statistics for a specific exercise"""
    try:
        # Check if exercise exists
        exercise_result = supabase.table("exercises").select("id, name").eq("id", exercise_id).execute()
        if not exercise_result.data:
            raise HTTPException(status_code=404, detail="Exercise not found")
        
        exercise_name = exercise_result.data[0]["name"]
        
        # Get exercise progress
        progress_result = supabase.table("progress").select("*").eq("exercise_id", exercise_id).execute()
        exercise_progress = progress_result.data
        personal_records = [p for p in exercise_progress if p.get("personal_record", False)]
        
        unique_users = len(set(p["user_id"] for p in exercise_progress))
        
        stats = {
            "exercise_id": exercise_id,
            "exercise_name": exercise_name,
            "total_attempts": len(exercise_progress),
            "unique_users": unique_users,
            "personal_records": len(personal_records),
            "average_weight": sum(p.get("weight_kg") or 0 for p in exercise_progress) / len(exercise_progress) if exercise_progress else 0,
            "average_reps": sum(p.get("reps") or 0 for p in exercise_progress) / len(exercise_progress) if exercise_progress else 0
        }
        
        return stats
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching exercise stats: {str(e)}")
