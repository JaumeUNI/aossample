# Guía de Ejecución Rápida - API de Rutinas Deportivas

## 🚀 Inicio Rápido

### 1. Preparación del Entorno

```bash
# Navegar al directorio del proyecto
cd C:\Users\jejej\OneDrive\Escritorio\github_projects\aossample

# Activar el entorno virtual
venv\Scripts\activate

# Verificar que las dependencias estén instaladas
pip list | findstr fastapi
```

### 2. Ejecutar el Servidor

```bash
# Opción 1: Usando uvicorn directamente
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Opción 2: Ejecutar desde Python
python app/main.py
```

### 3. Acceder a la Documentación

Una vez ejecutado el servidor, accede a:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **API Base**: http://127.0.0.1:8000

## 📋 Endpoints Disponibles

### 🏋️ Ejercicios (CRUD Completo)

#### ➕ Crear Ejercicio (POST)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/exercises" -Method POST -ContentType "application/json" -Body '{
    "name": "Push-ups",
    "description": "Classic bodyweight exercise",
    "exercise_type": "strength",
    "difficulty": "beginner",
    "muscle_groups": ["chest", "arms"],
    "duration_minutes": 5,
    "calories_burned_per_minute": 8,
    "equipment_needed": [],
    "instructions": ["Start in plank position", "Lower body to ground", "Push back up"]
}'
```

#### 📖 Obtener Todos los Ejercicios (GET)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/exercises" -Method GET
```

#### 🔍 Obtener Ejercicio Específico (GET)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/exercises/1" -Method GET
```

#### 🔄 Actualizar Ejercicio (PUT)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/exercises/1" -Method PUT -ContentType "application/json" -Body '{
    "name": "Modified Push-ups",
    "description": "Updated description",
    "exercise_type": "strength",
    "difficulty": "intermediate",
    "muscle_groups": ["chest", "arms", "core"]
}'
```

#### 🗑️ Eliminar Ejercicio (DELETE)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/exercises/1" -Method DELETE
```

### 🏃 Rutinas de Entrenamiento (CRUD Completo)

#### ➕ Crear Rutina (POST)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/routines" -Method POST -ContentType "application/json" -Body '{
    "name": "Beginner Full Body",
    "description": "Complete workout for beginners",
    "difficulty": "beginner",
    "target_muscle_groups": ["legs", "core"],
    "estimated_duration_minutes": 30,
    "exercises": [
        {"exercise_id": 1, "sets": 3, "reps": 15, "rest_seconds": 60},
        {"exercise_id": 2, "duration_minutes": 1, "rest_seconds": 30}
    ]
}'
```

#### 📖 Obtener Todas las Rutinas (GET)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/routines" -Method GET
```

#### 🔍 Obtener Rutina Específica (GET)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/routines/1" -Method GET
```

### 👤 Usuarios (CRUD Completo)

#### ➕ Crear Usuario (POST)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/users" -Method POST -ContentType "application/json" -Body '{
    "username": "john_doe",
    "email": "john@example.com",
    "age": 25,
    "weight_kg": 70.0,
    "height_cm": 175.0,
    "fitness_level": "beginner",
    "goals": ["lose_weight", "build_muscle"]
}'
```

#### 📖 Obtener Todos los Usuarios (GET)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/users" -Method GET
```

#### 🔍 Obtener Usuario Específico (GET)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/users/1" -Method GET
```

### 🏋️ Sesiones de Entrenamiento

#### ➕ Iniciar Sesión (POST)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/sessions" -Method POST -ContentType "application/json" -Body '{
    "user_id": 1,
    "routine_id": 1,
    "started_at": "2024-01-15T10:00:00"
}'
```

#### ✏️ Completar Sesión (PATCH)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/sessions/1" -Method PATCH -ContentType "application/json" -Body '{
    "completed": true,
    "total_duration_minutes": 25,
    "calories_burned": 200,
    "notes": "Great workout!"
}'
```

### 📈 Progreso del Usuario

#### ➕ Registrar Progreso (POST)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/progress" -Method POST -ContentType "application/json" -Body '{
    "user_id": 1,
    "exercise_id": 1,
    "weight_kg": 50.0,
    "reps": 10,
    "sets": 3,
    "personal_record": true
}'
```

#### 📊 Obtener Estadísticas de Usuario (GET)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/stats/user/1" -Method GET
```

#### 📊 Obtener Estadísticas de Ejercicio (GET)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/stats/exercise/1" -Method GET
```

## 🧪 Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
python -m pytest app/test/test_sample.py -v

# Ejecutar pruebas específicas
python -m pytest app/test/test_sample.py::test_create_exercise -v

# Ejecutar con cobertura
python -m pytest app/test/test_sample.py --cov=app
```

## 📝 Ejemplos de Uso

### Ejemplo 1: Flujo Completo de Fitness

```bash
# 1. Crear un ejercicio
Invoke-RestMethod -Uri "http://127.0.0.1:8000/exercises" -Method POST -ContentType "application/json" -Body '{
    "name": "Squats",
    "description": "Basic leg exercise",
    "exercise_type": "strength",
    "difficulty": "beginner",
    "muscle_groups": ["legs"]
}'

# 2. Crear un usuario
Invoke-RestMethod -Uri "http://127.0.0.1:8000/users" -Method POST -ContentType "application/json" -Body '{
    "username": "test_user",
    "email": "test@example.com",
    "fitness_level": "beginner"
}'

# 3. Crear una rutina
Invoke-RestMethod -Uri "http://127.0.0.1:8000/routines" -Method POST -ContentType "application/json" -Body '{
    "name": "Test Routine",
    "description": "Test routine",
    "difficulty": "beginner",
    "target_muscle_groups": ["legs"],
    "estimated_duration_minutes": 20
}'

# 4. Iniciar una sesión de entrenamiento
Invoke-RestMethod -Uri "http://127.0.0.1:8000/sessions" -Method POST -ContentType "application/json" -Body '{
    "user_id": 1,
    "routine_id": 1,
    "started_at": "2024-01-15T10:00:00"
}'

# 5. Registrar progreso
Invoke-RestMethod -Uri "http://127.0.0.1:8000/progress" -Method POST -ContentType "application/json" -Body '{
    "user_id": 1,
    "exercise_id": 1,
    "weight_kg": 30.0,
    "reps": 15,
    "sets": 3
}'
```

### Ejemplo 2: Filtros y Búsquedas

```bash
# Obtener ejercicios de fuerza
Invoke-RestMethod -Uri "http://127.0.0.1:8000/exercises?exercise_type=strength" -Method GET

# Obtener rutinas para principiantes
Invoke-RestMethod -Uri "http://127.0.0.1:8000/routines?difficulty=beginner" -Method GET

# Obtener progreso de un usuario específico
Invoke-RestMethod -Uri "http://127.0.0.1:8000/progress?user_id=1" -Method GET
```

### Ejemplo 3: Estadísticas y Analytics

```bash
# Obtener estadísticas de usuario
Invoke-RestMethod -Uri "http://127.0.0.1:8000/stats/user/1" -Method GET

# Obtener estadísticas de ejercicio
Invoke-RestMethod -Uri "http://127.0.0.1:8000/stats/exercise/1" -Method GET
```

## 🔧 Configuración Avanzada

### Variables de Entorno

```bash
# Cambiar puerto
uvicorn app.main:app --reload --port 8080

# Cambiar host (para acceso externo)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Modo de producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Logging

```bash
# Ejecutar con logging detallado
uvicorn app.main:app --reload --log-level debug
```

## 🐛 Solución de Problemas

### Error: Puerto en Uso
```bash
# Cambiar a otro puerto
uvicorn app.main:app --reload --port 8001
```

### Error: Módulo no Encontrado
```bash
# Verificar que el entorno virtual esté activado
venv\Scripts\activate

# Reinstalar dependencias
pip install -r app/requirements.txt
```

### Error: Pruebas Fallan
```bash
# Limpiar cache de pytest
python -m pytest --cache-clear

# Ejecutar con más verbosidad
python -m pytest app/test/test_sample.py -vv
```

## 📊 Monitoreo

### Verificar Estado del Servidor
```bash
# Health check simple
Invoke-RestMethod -Uri "http://127.0.0.1:8000/docs" -Method GET
```

### Ver Datos Almacenados
```bash
# Ver todos los ejercicios
Invoke-RestMethod -Uri "http://127.0.0.1:8000/exercises" -Method GET

# Ver todos los usuarios
Invoke-RestMethod -Uri "http://127.0.0.1:8000/users" -Method GET

# Ver todas las rutinas
Invoke-RestMethod -Uri "http://127.0.0.1:8000/routines" -Method GET
```

## 🎯 Próximos Pasos

1. **Explorar la Documentación**: Visita http://127.0.0.1:8000/docs
2. **Ejecutar Pruebas**: Verifica que todo funciona correctamente
3. **Experimentar con la API**: Prueba diferentes funcionalidades de fitness
4. **Revisar Código**: Explora la implementación en `app/routes/sample.py`

## 📚 Recursos Adicionales

- **Documentación FastAPI**: https://fastapi.tiangolo.com/
- **Documentación Pydantic**: https://pydantic-docs.helpmanual.io/
- **Documentación pytest**: https://docs.pytest.org/

---

¡Tu API de Rutinas Deportivas está lista para usar! 🏋️‍♂️🎉
