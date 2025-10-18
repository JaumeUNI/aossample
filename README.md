# ARQUITECTURA ORIENTADA A SERVICIOS 
## Curso 2025-26 
## FastAPI Project - Sistema de Rutinas Deportivas

# Sistema de Gestión de Rutinas Deportivas

Este es un sistema completo de gestión de fitness desarrollado con FastAPI que incluye funcionalidades CRUD completas para:
- **Ejercicios**: Gestión de ejercicios con clasificación por tipo, dificultad y grupos musculares
- **Rutinas de Entrenamiento**: Creación y gestión de rutinas personalizadas
- **Usuarios**: Registro y seguimiento de usuarios del sistema
- **Sesiones de Entrenamiento**: Inicio, seguimiento y finalización de workouts
- **Seguimiento de Progreso**: Registro de mejoras y récords personales
- **Analytics**: Estadísticas automáticas de usuarios y ejercicios

## Estructura del Proyecto

```bash
aossample/
│
├── app/
│   ├── __init__.py           # Inicializa la aplicación como paquete
│   ├── main.py               # Punto de entrada principal de la aplicación FastAPI
│   ├── routes/
│   │   ├── __init__.py       # Inicializa las rutas como paquete
│   │   └── sample.py         # Contiene todas las rutas de la API de fitness
│   ├── models/
│   │   ├── __init__.py       
│   │   └── item.py           # Define los modelos de datos usando Pydantic
│   ├── test/
│   │   ├── __init__.py       
│   │   └── test_sample.py    # Contiene las pruebas unitarias para la API
│   └── requirements.txt      # Dependencias del proyecto
│
├── venv/                     # Entorno virtual de Python
├── README.md                 # Documentación del proyecto
├── CAMBIOS_REALIZADOS.md     # Documentación de cambios implementados
└── GUIA_EJECUCION_RAPIDA.md  # Guía de ejecución rápida
```

## Configuración del Proyecto

### 1. **Clonar el Proyecto**

Primero, clona el repositorio del proyecto en tu máquina local:

```bash
git clone https://github.com/mcastrol/aossample.git
cd aossample
```

### 2. **Crear y Activar un Entorno Virtual de Python**

Crea un entorno virtual para gestionar las dependencias. Esto asegura que los paquetes específicos del proyecto estén aislados de tu entorno global de Python.

**En Linux/macOS**:
```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. **Instalar Dependencias desde `requirements.txt`**

Una vez que el entorno virtual esté activado, instala las dependencias del proyecto usando `requirements.txt`.

```bash
pip install -r app/requirements.txt
```

Esto instalará todos los paquetes necesarios como FastAPI, Uvicorn y Pytest.

### 4. **Ejecutar la Aplicación FastAPI**

Para ejecutar la aplicación FastAPI, usa el siguiente comando:

```bash
uvicorn app.main:app --reload
```

La opción `--reload` es útil en modo de desarrollo porque recarga la aplicación cuando se hacen cambios en el código.

Por defecto, la aplicación estará disponible en `http://127.0.0.1:8000`. Puedes acceder a la documentación de la API a través de:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### 5. **Probar la API con `pytest`**

Las pruebas unitarias para la API están incluidas en el archivo `app/test/test_sample.py`. Puedes ejecutar las pruebas usando `pytest`.

Para ejecutar las pruebas, simplemente ejecuta:

```bash
python -m pytest
```

## Endpoints de la API

### 🏋️ **Ejercicios**

#### POST `/exercises`
- **Descripción**: Crea un nuevo ejercicio con clasificación completa
- **Request Body**:
  ```json
  {
    "name": "Push-ups",
    "description": "Classic bodyweight exercise",
    "exercise_type": "strength",
    "difficulty": "beginner",
    "muscle_groups": ["chest", "arms"],
    "duration_minutes": 5,
    "calories_burned_per_minute": 8,
    "equipment_needed": [],
    "instructions": ["Start in plank position", "Lower body to ground", "Push back up"]
  }
  ```

#### GET `/exercises`
- **Descripción**: Obtiene todos los ejercicios con filtros opcionales
- **Query Parameters**:
  - `exercise_type`: cardio, strength, flexibility, balance, sports
  - `difficulty`: beginner, intermediate, advanced
  - `muscle_group`: chest, back, shoulders, arms, legs, core, full_body

#### GET `/exercises/{exercise_id}`
- **Descripción**: Obtiene un ejercicio específico por ID

### 🏃 **Rutinas de Entrenamiento**

#### POST `/routines`
- **Descripción**: Crea una nueva rutina de entrenamiento
- **Request Body**:
  ```json
  {
    "name": "Beginner Full Body",
    "description": "Complete workout for beginners",
    "difficulty": "beginner",
    "target_muscle_groups": ["legs", "core"],
    "estimated_duration_minutes": 30,
    "exercises": [
      {"exercise_id": 1, "sets": 3, "reps": 15, "rest_seconds": 60}
    ]
  }
  ```

#### GET `/routines`
- **Descripción**: Obtiene todas las rutinas con filtros opcionales

### 👤 **Usuarios**

#### POST `/users`
- **Descripción**: Registra un nuevo usuario
- **Request Body**:
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "age": 25,
    "weight_kg": 70.0,
    "height_cm": 175.0,
    "fitness_level": "beginner",
    "goals": ["lose_weight", "build_muscle"]
  }
  ```

### 🏋️ **Sesiones de Entrenamiento**

#### POST `/sessions`
- **Descripción**: Inicia una nueva sesión de entrenamiento
- **Request Body**:
  ```json
  {
    "user_id": 1,
    "routine_id": 1,
    "started_at": "2024-01-15T10:00:00"
  }
  ```

#### PATCH `/sessions/{session_id}`
- **Descripción**: Completa o actualiza una sesión de entrenamiento

### 📈 **Progreso del Usuario**

#### POST `/progress`
- **Descripción**: Registra el progreso del usuario en un ejercicio
- **Request Body**:
  ```json
  {
    "user_id": 1,
    "exercise_id": 1,
    "weight_kg": 50.0,
    "reps": 10,
    "sets": 3,
    "personal_record": true
  }
  ```

### 📊 **Analytics y Estadísticas**

#### GET `/stats/user/{user_id}`
- **Descripción**: Obtiene estadísticas completas de un usuario

#### GET `/stats/exercise/{exercise_id}`
- **Descripción**: Obtiene estadísticas de uso de un ejercicio

## Características Principales

### ✅ **Funcionalidades Implementadas**
- **CRUD Completo**: Create, Read, Update, Delete para todas las entidades
- **Validación Robusta**: Validación automática de datos con Pydantic
- **Filtros Avanzados**: Búsqueda por tipo, dificultad, grupo muscular
- **Analytics Automáticos**: Estadísticas de usuarios y ejercicios
- **Seguimiento de Progreso**: Registro de mejoras y récords personales
- **API RESTful**: Endpoints bien estructurados y documentados

### 🧪 **Testing**
- **30+ Pruebas**: Cobertura completa de todas las funcionalidades
- **Pruebas de Casos Edge**: Validación de errores y casos límite
- **Pruebas de Relaciones**: Validación de relaciones entre entidades

### 📚 **Documentación**
- **Swagger UI**: Documentación interactiva en `/docs`
- **ReDoc**: Documentación alternativa en `/redoc`
- **Guías Completas**: Documentación de cambios y guía de ejecución

## Comandos Útiles

### Generar `requirements.txt`
Para generar un archivo `requirements.txt` después de agregar nuevas dependencias:

```bash
pip freeze > app/requirements.txt
```

### Ejecutar Pruebas Específicas
```bash
# Todas las pruebas
python -m pytest app/test/test_sample.py -v

# Pruebas específicas
python -m pytest app/test/test_sample.py::test_create_exercise -v
```

---

