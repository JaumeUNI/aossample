from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class ExerciseType(str, Enum):
    CARDIO = "cardio"
    STRENGTH = "strength"
    FLEXIBILITY = "flexibility"
    BALANCE = "balance"
    SPORTS = "sports"

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class MuscleGroup(str, Enum):
    CHEST = "chest"
    BACK = "back"
    SHOULDERS = "shoulders"
    ARMS = "arms"
    LEGS = "legs"
    CORE = "core"
    FULL_BODY = "full_body"

class Exercise(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    exercise_type: ExerciseType
    difficulty: DifficultyLevel
    muscle_groups: List[MuscleGroup]
    duration_minutes: Optional[int] = None
    calories_burned_per_minute: Optional[int] = None
    equipment_needed: List[str] = []
    instructions: List[str] = []

class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    exercise_type: Optional[ExerciseType] = None
    difficulty: Optional[DifficultyLevel] = None
    muscle_groups: Optional[List[MuscleGroup]] = None
    duration_minutes: Optional[int] = None
    calories_burned_per_minute: Optional[int] = None
    equipment_needed: Optional[List[str]] = None
    instructions: Optional[List[str]] = None

class ExerciseInRoutine(BaseModel):
    exercise_id: int
    sets: Optional[int] = None
    reps: Optional[int] = None
    duration_minutes: Optional[int] = None
    rest_seconds: Optional[int] = 60
    weight_kg: Optional[float] = None

class WorkoutRoutine(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    difficulty: DifficultyLevel
    target_muscle_groups: List[MuscleGroup]
    estimated_duration_minutes: int
    exercises: List[ExerciseInRoutine] = []
    created_at: Optional[datetime] = None
    created_by: Optional[str] = "admin"

class WorkoutRoutineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    target_muscle_groups: Optional[List[MuscleGroup]] = None
    estimated_duration_minutes: Optional[int] = None
    exercises: Optional[List[ExerciseInRoutine]] = None

class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    fitness_level: DifficultyLevel = DifficultyLevel.BEGINNER
    goals: List[str] = []
    created_at: Optional[datetime] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    fitness_level: Optional[DifficultyLevel] = None
    goals: Optional[List[str]] = None

class WorkoutSession(BaseModel):
    id: Optional[int] = None
    user_id: int
    routine_id: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    total_duration_minutes: Optional[int] = None
    calories_burned: Optional[int] = None
    notes: Optional[str] = None
    completed: bool = False

class WorkoutSessionUpdate(BaseModel):
    completed_at: Optional[datetime] = None
    total_duration_minutes: Optional[int] = None
    calories_burned: Optional[int] = None
    notes: Optional[str] = None
    completed: Optional[bool] = None

class UserProgress(BaseModel):
    id: Optional[int] = None
    user_id: int
    exercise_id: int
    date: Optional[datetime] = None
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    sets: Optional[int] = None
    duration_minutes: Optional[int] = None
    personal_record: bool = False

class UserProgressUpdate(BaseModel):
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    sets: Optional[int] = None
    duration_minutes: Optional[int] = None
    personal_record: Optional[bool] = None
