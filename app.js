// API Base URL - Auto-detect based on environment
const API_BASE_URL = window.location.origin;

// ========== TAB NAVIGATION ==========
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tabs
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
            
            // Load data for the active tab
            loadTabData(targetTab);
        });
    });

    // Load initial data
    loadTabData('exercises');
});

function loadTabData(tab) {
    switch(tab) {
        case 'exercises':
            loadExercises();
            break;
        case 'routines':
            loadRoutines();
            break;
        case 'users':
            loadUsers();
            break;
        case 'sessions':
            loadSessions();
            break;
        case 'progress':
            loadProgress();
            break;
    }
}

// ========== EXERCISES ==========
function showExerciseForm() {
    document.getElementById('exercise-form').style.display = 'block';
    document.getElementById('exercise-form-title').textContent = 'Crear Nuevo Ejercicio';
    document.getElementById('exercise-form-element').reset();
    document.getElementById('exercise-form-element').onsubmit = handleExerciseSubmit;
}

function hideExerciseForm() {
    document.getElementById('exercise-form').style.display = 'none';
}

async function handleExerciseSubmit(event) {
    event.preventDefault();
    
    const muscleGroups = Array.from(document.querySelectorAll('#exercise-form input[type="checkbox"]:checked'))
        .map(cb => cb.value);
    
    const equipment = document.getElementById('exercise-equipment').value
        .split(',')
        .map(item => item.trim())
        .filter(item => item);
    
    const instructions = document.getElementById('exercise-instructions').value
        .split('\n')
        .map(inst => inst.trim())
        .filter(inst => inst);
    
    const exerciseData = {
        name: document.getElementById('exercise-name').value,
        description: document.getElementById('exercise-description').value,
        exercise_type: document.getElementById('exercise-type').value,
        difficulty: document.getElementById('exercise-difficulty').value,
        muscle_groups: muscleGroups,
        duration_minutes: document.getElementById('exercise-duration').value ? 
            parseInt(document.getElementById('exercise-duration').value) : null,
        calories_burned_per_minute: document.getElementById('exercise-calories').value ? 
            parseInt(document.getElementById('exercise-calories').value) : null,
        equipment_needed: equipment,
        instructions: instructions
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/exercises`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(exerciseData)
        });
        
        if (response.ok) {
            const exercise = await response.json();
            alert('Ejercicio creado exitosamente!');
            hideExerciseForm();
            loadExercises();
        } else {
            const error = await response.json();
            alert('Error: ' + (error.detail || 'No se pudo crear el ejercicio'));
        }
    } catch (error) {
        alert('Error de conexión: ' + error.message);
    }
}

async function loadExercises() {
    const typeFilter = document.getElementById('filter-type')?.value || '';
    const difficultyFilter = document.getElementById('filter-difficulty')?.value || '';
    const muscleFilter = document.getElementById('filter-muscle')?.value || '';
    
    let url = `${API_BASE_URL}/exercises?`;
    const params = [];
    if (typeFilter) params.push(`exercise_type=${typeFilter}`);
    if (difficultyFilter) params.push(`difficulty=${difficultyFilter}`);
    if (muscleFilter) params.push(`muscle_group=${muscleFilter}`);
    
    url += params.join('&');
    
    const container = document.getElementById('exercises-list');
    container.innerHTML = '<div class="loading">Cargando ejercicios...</div>';
    
    try {
        const response = await fetch(url);
        const exercises = await response.json();
        
        if (exercises.length === 0) {
            container.innerHTML = '<div class="empty-state"><h3>No hay ejercicios</h3><p>Crea tu primer ejercicio usando el botón de arriba</p></div>';
            return;
        }
        
        container.innerHTML = exercises.map(exercise => `
            <div class="card">
                <div class="card-header">
                    <div>
                        <div class="card-title">${exercise.name}</div>
                        <div class="card-id">ID: ${exercise.id}</div>
                    </div>
                </div>
                <div class="card-body">
                    <p><strong>Descripción:</strong> ${exercise.description}</p>
                    <p><strong>Tipo:</strong> ${translateExerciseType(exercise.exercise_type)}</p>
                    <p><strong>Dificultad:</strong> <span class="badge badge-${exercise.difficulty}">${translateDifficulty(exercise.difficulty)}</span></p>
                    ${exercise.duration_minutes ? `<p><strong>Duración:</strong> ${exercise.duration_minutes} minutos</p>` : ''}
                    ${exercise.calories_burned_per_minute ? `<p><strong>Calorías/min:</strong> ${exercise.calories_burned_per_minute}</p>` : ''}
                    ${exercise.muscle_groups.length > 0 ? `<p><strong>Grupos musculares:</strong> ${exercise.muscle_groups.map(mg => translateMuscleGroup(mg)).join(', ')}</p>` : ''}
                    ${exercise.equipment_needed.length > 0 ? `<p><strong>Equipamiento:</strong> ${exercise.equipment_needed.join(', ')}</p>` : ''}
                    ${exercise.instructions.length > 0 ? `<p><strong>Instrucciones:</strong><br>${exercise.instructions.map((inst, i) => `${i+1}. ${inst}`).join('<br>')}</p>` : ''}
                </div>
                <div class="card-tags">
                    <span class="tag tag-primary">${translateExerciseType(exercise.exercise_type)}</span>
                    <span class="tag badge-${exercise.difficulty}">${translateDifficulty(exercise.difficulty)}</span>
                </div>
                <div class="card-actions">
                    <button class="btn btn-danger" onclick="deleteExercise(${exercise.id})">Eliminar</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = `<div class="empty-state"><h3>Error</h3><p>No se pudo cargar los ejercicios: ${error.message}</p></div>`;
    }
}

async function deleteExercise(id) {
    if (!confirm('¿Estás seguro de que quieres eliminar este ejercicio?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/exercises/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Ejercicio eliminado exitosamente');
            loadExercises();
        } else {
            const error = await response.json();
            alert('Error: ' + (error.detail || 'No se pudo eliminar el ejercicio'));
        }
    } catch (error) {
        alert('Error de conexión: ' + error.message);
    }
}

// ========== ROUTINES ==========
function showRoutineForm() {
    document.getElementById('routine-form').style.display = 'block';
    document.getElementById('routine-form-element').reset();
}

function hideRoutineForm() {
    document.getElementById('routine-form').style.display = 'none';
}

async function handleRoutineSubmit(event) {
    event.preventDefault();
    
    const targetMuscleGroups = Array.from(document.querySelectorAll('#routine-form input[type="checkbox"]:checked'))
        .map(cb => cb.value);
    
    const routineData = {
        name: document.getElementById('routine-name').value,
        description: document.getElementById('routine-description').value,
        difficulty: document.getElementById('routine-difficulty').value,
        target_muscle_groups: targetMuscleGroups,
        estimated_duration_minutes: parseInt(document.getElementById('routine-duration').value),
        exercises: []
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/routines`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(routineData)
        });
        
        if (response.ok) {
            const routine = await response.json();
            alert('Rutina creada exitosamente!');
            hideRoutineForm();
            loadRoutines();
        } else {
            const error = await response.json();
            alert('Error: ' + (error.detail || 'No se pudo crear la rutina'));
        }
    } catch (error) {
        alert('Error de conexión: ' + error.message);
    }
}

async function loadRoutines() {
    const container = document.getElementById('routines-list');
    container.innerHTML = '<div class="loading">Cargando rutinas...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/routines`);
        const routines = await response.json();
        
        if (routines.length === 0) {
            container.innerHTML = '<div class="empty-state"><h3>No hay rutinas</h3><p>Crea tu primera rutina usando el botón de arriba</p></div>';
            return;
        }
        
        container.innerHTML = routines.map(routine => `
            <div class="card">
                <div class="card-header">
                    <div>
                        <div class="card-title">${routine.name}</div>
                        <div class="card-id">ID: ${routine.id}</div>
                    </div>
                </div>
                <div class="card-body">
                    <p><strong>Descripción:</strong> ${routine.description}</p>
                    <p><strong>Dificultad:</strong> <span class="badge badge-${routine.difficulty}">${translateDifficulty(routine.difficulty)}</span></p>
                    <p><strong>Duración estimada:</strong> ${routine.estimated_duration_minutes} minutos</p>
                    ${routine.target_muscle_groups.length > 0 ? `<p><strong>Grupos musculares objetivo:</strong> ${routine.target_muscle_groups.map(mg => translateMuscleGroup(mg)).join(', ')}</p>` : ''}
                    <p><strong>Ejercicios incluidos:</strong> ${routine.exercises.length}</p>
                    ${routine.created_at ? `<p><strong>Creada:</strong> ${new Date(routine.created_at).toLocaleString('es-ES')}</p>` : ''}
                </div>
                <div class="card-tags">
                    <span class="tag badge-${routine.difficulty}">${translateDifficulty(routine.difficulty)}</span>
                    <span class="tag tag-primary">${routine.estimated_duration_minutes} min</span>
                </div>
                <div class="card-actions">
                    <button class="btn btn-danger" onclick="deleteRoutine(${routine.id})">Eliminar</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = `<div class="empty-state"><h3>Error</h3><p>No se pudo cargar las rutinas: ${error.message}</p></div>`;
    }
}

async function deleteRoutine(id) {
    if (!confirm('¿Estás seguro de que quieres eliminar esta rutina?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/routines/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Rutina eliminada exitosamente');
            loadRoutines();
        } else {
            const error = await response.json();
            alert('Error: ' + (error.detail || 'No se pudo eliminar la rutina'));
        }
    } catch (error) {
        alert('Error de conexión: ' + error.message);
    }
}

// ========== USERS ==========
function showUserForm() {
    document.getElementById('user-form').style.display = 'block';
    document.getElementById('user-form-element').reset();
}

function hideUserForm() {
    document.getElementById('user-form').style.display = 'none';
}

async function handleUserSubmit(event) {
    event.preventDefault();
    
    const goals = document.getElementById('user-goals').value
        .split(',')
        .map(goal => goal.trim())
        .filter(goal => goal);
    
    const userData = {
        username: document.getElementById('user-username').value,
        email: document.getElementById('user-email').value,
        age: document.getElementById('user-age').value ? parseInt(document.getElementById('user-age').value) : null,
        weight_kg: document.getElementById('user-weight').value ? parseFloat(document.getElementById('user-weight').value) : null,
        height_cm: document.getElementById('user-height').value ? parseFloat(document.getElementById('user-height').value) : null,
        fitness_level: document.getElementById('user-fitness-level').value,
        goals: goals
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        if (response.ok) {
            const user = await response.json();
            alert('Usuario registrado exitosamente!');
            hideUserForm();
            loadUsers();
        } else {
            const error = await response.json();
            alert('Error: ' + (error.detail || 'No se pudo registrar el usuario'));
        }
    } catch (error) {
        alert('Error de conexión: ' + error.message);
    }
}

async function loadUsers() {
    const container = document.getElementById('users-list');
    container.innerHTML = '<div class="loading">Cargando usuarios...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/users`);
        const users = await response.json();
        
        if (users.length === 0) {
            container.innerHTML = '<div class="empty-state"><h3>No hay usuarios</h3><p>Registra tu primer usuario usando el botón de arriba</p></div>';
            return;
        }
        
        container.innerHTML = users.map(user => `
            <div class="card">
                <div class="card-header">
                    <div>
                        <div class="card-title">${user.username}</div>
                        <div class="card-id">ID: ${user.id}</div>
                    </div>
                </div>
                <div class="card-body">
                    <p><strong>Email:</strong> ${user.email}</p>
                    ${user.age ? `<p><strong>Edad:</strong> ${user.age} años</p>` : ''}
                    ${user.weight_kg ? `<p><strong>Peso:</strong> ${user.weight_kg} kg</p>` : ''}
                    ${user.height_cm ? `<p><strong>Altura:</strong> ${user.height_cm} cm</p>` : ''}
                    <p><strong>Nivel de fitness:</strong> <span class="badge badge-${user.fitness_level}">${translateDifficulty(user.fitness_level)}</span></p>
                    ${user.goals.length > 0 ? `<p><strong>Objetivos:</strong> ${user.goals.join(', ')}</p>` : ''}
                    ${user.created_at ? `<p><strong>Registrado:</strong> ${new Date(user.created_at).toLocaleString('es-ES')}</p>` : ''}
                </div>
                <div class="card-tags">
                    <span class="tag badge-${user.fitness_level}">${translateDifficulty(user.fitness_level)}</span>
                </div>
                <div class="card-actions">
                    <button class="btn btn-danger" onclick="deleteUser(${user.id})">Eliminar</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = `<div class="empty-state"><h3>Error</h3><p>No se pudo cargar los usuarios: ${error.message}</p></div>`;
    }
}

async function deleteUser(id) {
    if (!confirm('¿Estás seguro de que quieres eliminar este usuario?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Usuario eliminado exitosamente');
            loadUsers();
        } else {
            const error = await response.json();
            alert('Error: ' + (error.detail || 'No se pudo eliminar el usuario'));
        }
    } catch (error) {
        alert('Error de conexión: ' + error.message);
    }
}

// ========== SESSIONS ==========
function showSessionForm() {
    document.getElementById('session-form').style.display = 'block';
    document.getElementById('session-form-element').reset();
}

function hideSessionForm() {
    document.getElementById('session-form').style.display = 'none';
}

async function handleSessionSubmit(event) {
    event.preventDefault();
    
    const sessionData = {
        user_id: parseInt(document.getElementById('session-user-id').value),
        routine_id: parseInt(document.getElementById('session-routine-id').value),
        started_at: new Date().toISOString()
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/sessions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(sessionData)
        });
        
        if (response.ok) {
            const session = await response.json();
            alert('Sesión iniciada exitosamente!');
            hideSessionForm();
            loadSessions();
        } else {
            const error = await response.json();
            alert('Error: ' + (error.detail || 'No se pudo iniciar la sesión'));
        }
    } catch (error) {
        alert('Error de conexión: ' + error.message);
    }
}

async function loadSessions() {
    const container = document.getElementById('sessions-list');
    container.innerHTML = '<div class="loading">Cargando sesiones...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/sessions`);
        const sessions = await response.json();
        
        if (sessions.length === 0) {
            container.innerHTML = '<div class="empty-state"><h3>No hay sesiones</h3><p>Inicia tu primera sesión usando el botón de arriba</p></div>';
            return;
        }
        
        container.innerHTML = sessions.map(session => `
            <div class="card">
                <div class="card-header">
                    <div>
                        <div class="card-title">Sesión #${session.id}</div>
                        <div class="card-id">Usuario ID: ${session.user_id} | Rutina ID: ${session.routine_id}</div>
                    </div>
                </div>
                <div class="card-body">
                    <p><strong>Estado:</strong> ${session.completed ? '<span class="badge badge-success">Completada</span>' : '<span class="badge badge-warning">En progreso</span>'}</p>
                    <p><strong>Iniciada:</strong> ${new Date(session.started_at).toLocaleString('es-ES')}</p>
                    ${session.completed_at ? `<p><strong>Completada:</strong> ${new Date(session.completed_at).toLocaleString('es-ES')}</p>` : ''}
                    ${session.total_duration_minutes ? `<p><strong>Duración:</strong> ${session.total_duration_minutes} minutos</p>` : ''}
                    ${session.calories_burned ? `<p><strong>Calorías quemadas:</strong> ${session.calories_burned}</p>` : ''}
                    ${session.notes ? `<p><strong>Notas:</strong> ${session.notes}</p>` : ''}
                </div>
                <div class="card-tags">
                    ${session.completed ? '<span class="tag tag-success">Completada</span>' : '<span class="tag tag-warning">En progreso</span>'}
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = `<div class="empty-state"><h3>Error</h3><p>No se pudo cargar las sesiones: ${error.message}</p></div>`;
    }
}

// ========== PROGRESS ==========
function showProgressForm() {
    document.getElementById('progress-form').style.display = 'block';
    document.getElementById('progress-form-element').reset();
}

function hideProgressForm() {
    document.getElementById('progress-form').style.display = 'none';
}

async function handleProgressSubmit(event) {
    event.preventDefault();
    
    const progressData = {
        user_id: parseInt(document.getElementById('progress-user-id').value),
        exercise_id: parseInt(document.getElementById('progress-exercise-id').value),
        weight_kg: document.getElementById('progress-weight').value ? parseFloat(document.getElementById('progress-weight').value) : null,
        reps: document.getElementById('progress-reps').value ? parseInt(document.getElementById('progress-reps').value) : null,
        sets: document.getElementById('progress-sets').value ? parseInt(document.getElementById('progress-sets').value) : null,
        duration_minutes: document.getElementById('progress-duration').value ? parseInt(document.getElementById('progress-duration').value) : null,
        personal_record: document.getElementById('progress-record').checked
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/progress`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(progressData)
        });
        
        if (response.ok) {
            const progress = await response.json();
            alert('Progreso registrado exitosamente!');
            hideProgressForm();
            loadProgress();
        } else {
            const error = await response.json();
            alert('Error: ' + (error.detail || 'No se pudo registrar el progreso'));
        }
    } catch (error) {
        alert('Error de conexión: ' + error.message);
    }
}

async function loadProgress() {
    const container = document.getElementById('progress-list');
    container.innerHTML = '<div class="loading">Cargando progreso...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/progress`);
        const progressList = await response.json();
        
        if (progressList.length === 0) {
            container.innerHTML = '<div class="empty-state"><h3>No hay registros de progreso</h3><p>Registra tu primer progreso usando el botón de arriba</p></div>';
            return;
        }
        
        container.innerHTML = progressList.map(progress => `
            <div class="card">
                <div class="card-header">
                    <div>
                        <div class="card-title">Registro #${progress.id}</div>
                        <div class="card-id">Usuario ID: ${progress.user_id} | Ejercicio ID: ${progress.exercise_id}</div>
                    </div>
                </div>
                <div class="card-body">
                    ${progress.date ? `<p><strong>Fecha:</strong> ${new Date(progress.date).toLocaleString('es-ES')}</p>` : ''}
                    ${progress.weight_kg ? `<p><strong>Peso:</strong> ${progress.weight_kg} kg</p>` : ''}
                    ${progress.reps ? `<p><strong>Repeticiones:</strong> ${progress.reps}</p>` : ''}
                    ${progress.sets ? `<p><strong>Series:</strong> ${progress.sets}</p>` : ''}
                    ${progress.duration_minutes ? `<p><strong>Duración:</strong> ${progress.duration_minutes} minutos</p>` : ''}
                    <p><strong>Récord personal:</strong> ${progress.personal_record ? '<span class="badge badge-success">Sí</span>' : '<span class="badge">No</span>'}</p>
                </div>
                <div class="card-tags">
                    ${progress.personal_record ? '<span class="tag tag-success">🏆 Récord</span>' : ''}
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = `<div class="empty-state"><h3>Error</h3><p>No se pudo cargar el progreso: ${error.message}</p></div>`;
    }
}

// ========== TRANSLATION HELPERS ==========
function translateExerciseType(type) {
    const translations = {
        'strength': 'Fuerza',
        'cardio': 'Cardio',
        'flexibility': 'Flexibilidad',
        'balance': 'Equilibrio',
        'sports': 'Deportes'
    };
    return translations[type] || type;
}

function translateDifficulty(difficulty) {
    const translations = {
        'beginner': 'Principiante',
        'intermediate': 'Intermedio',
        'advanced': 'Avanzado'
    };
    return translations[difficulty] || difficulty;
}

function translateMuscleGroup(group) {
    const translations = {
        'chest': 'Pecho',
        'back': 'Espalda',
        'shoulders': 'Hombros',
        'arms': 'Brazos',
        'legs': 'Piernas',
        'core': 'Core',
        'full_body': 'Cuerpo Completo'
    };
    return translations[group] || group;
}

