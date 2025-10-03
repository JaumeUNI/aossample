# Guía de Ejecución Rápida - API de Operaciones Aritméticas

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

### Operaciones Aritméticas (CRUD Completo)

#### ➕ Crear Operación (POST)
```bash
curl -X POST "http://127.0.0.1:8000/arithmetic" \
     -H "Content-Type: application/json" \
     -d '{"operation": "add", "value1": 10.0, "value2": 5.0}'
```

#### 📖 Obtener Todas las Operaciones (GET)
```bash
curl -X GET "http://127.0.0.1:8000/arithmetic"
```

#### 🔍 Obtener Operación Específica (GET)
```bash
curl -X GET "http://127.0.0.1:8000/arithmetic/1"
```

#### 🔄 Actualizar Operación Completa (PUT)
```bash
curl -X PUT "http://127.0.0.1:8000/arithmetic/1" \
     -H "Content-Type: application/json" \
     -d '{"operation": "multiply", "value1": 3.0, "value2": 7.0}'
```

#### ✏️ Actualizar Operación Parcial (PATCH)
```bash
curl -X PATCH "http://127.0.0.1:8000/arithmetic/1" \
     -H "Content-Type: application/json" \
     -d '{"operation": "divide", "value1": 21.0}'
```

#### 🗑️ Eliminar Operación Específica (DELETE)
```bash
curl -X DELETE "http://127.0.0.1:8000/arithmetic/1"
```

#### 🧹 Eliminar Todas las Operaciones (DELETE)
```bash
curl -X DELETE "http://127.0.0.1:8000/arithmetic"
```

### Funcionalidades Originales

#### ➕ Procesar Datos (POST)
```bash
curl -X POST "http://127.0.0.1:8000/process" \
     -H "Content-Type: application/json" \
     -d '{"value1": 10, "value2": 5}'
```

#### 🔗 Concatenar Strings (GET)
```bash
curl -X GET "http://127.0.0.1:8000/concat?param1=Hello&param2=World"
```

#### 📏 Longitud de String (GET)
```bash
curl -X GET "http://127.0.0.1:8000/length?string=FastAPI"
```

## 🧪 Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
python -m pytest app/test/test_sample.py -v

# Ejecutar pruebas específicas
python -m pytest app/test/test_sample.py::test_create_addition -v

# Ejecutar con cobertura
python -m pytest app/test/test_sample.py --cov=app
```

## 📝 Ejemplos de Uso

### Ejemplo 1: Flujo Completo CRUD

```bash
# 1. Crear una operación de suma
curl -X POST "http://127.0.0.1:8000/arithmetic" \
     -H "Content-Type: application/json" \
     -d '{"operation": "add", "value1": 15.0, "value2": 25.0}'

# Respuesta: {"id": 1, "operation": "add", "value1": 15.0, "value2": 25.0, "result": 40.0, "timestamp": "2024-..."}

# 2. Obtener la operación creada
curl -X GET "http://127.0.0.1:8000/arithmetic/1"

# 3. Actualizar la operación (cambiar a multiplicación)
curl -X PUT "http://127.0.0.1:8000/arithmetic/1" \
     -H "Content-Type: application/json" \
     -d '{"operation": "multiply", "value1": 15.0, "value2": 25.0}'

# 4. Actualizar parcialmente (solo cambiar el segundo valor)
curl -X PATCH "http://127.0.0.1:8000/arithmetic/1" \
     -H "Content-Type: application/json" \
     -d '{"value2": 3.0}'

# 5. Eliminar la operación
curl -X DELETE "http://127.0.0.1:8000/arithmetic/1"
```

### Ejemplo 2: Operaciones Aritméticas

```bash
# Suma
curl -X POST "http://127.0.0.1:8000/arithmetic" \
     -H "Content-Type: application/json" \
     -d '{"operation": "add", "value1": 10.0, "value2": 5.0}'

# Resta
curl -X POST "http://127.0.0.1:8000/arithmetic" \
     -H "Content-Type: application/json" \
     -d '{"operation": "subtract", "value1": 10.0, "value2": 3.0}'

# Multiplicación
curl -X POST "http://127.0.0.1:8000/arithmetic" \
     -H "Content-Type: application/json" \
     -d '{"operation": "multiply", "value1": 4.0, "value2": 5.0}'

# División
curl -X POST "http://127.0.0.1:8000/arithmetic" \
     -H "Content-Type: application/json" \
     -d '{"operation": "divide", "value1": 15.0, "value2": 3.0}'
```

### Ejemplo 3: Manejo de Errores

```bash
# División por cero (debería devolver error 400)
curl -X POST "http://127.0.0.1:8000/arithmetic" \
     -H "Content-Type: application/json" \
     -d '{"operation": "divide", "value1": 10.0, "value2": 0.0}'

# Operación no encontrada (debería devolver error 404)
curl -X GET "http://127.0.0.1:8000/arithmetic/999"

# Operación inválida (debería devolver error 400)
curl -X POST "http://127.0.0.1:8000/arithmetic" \
     -H "Content-Type: application/json" \
     -d '{"operation": "invalid", "value1": 10.0, "value2": 5.0}'
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
curl -X GET "http://127.0.0.1:8000/docs"
```

### Ver Operaciones Almacenadas
```bash
# Ver todas las operaciones
curl -X GET "http://127.0.0.1:8000/arithmetic" | python -m json.tool
```

## 🎯 Próximos Pasos

1. **Explorar la Documentación**: Visita http://127.0.0.1:8000/docs
2. **Ejecutar Pruebas**: Verifica que todo funciona correctamente
3. **Experimentar con la API**: Prueba diferentes operaciones aritméticas
4. **Revisar Código**: Explora la implementación en `app/routes/sample.py`

## 📚 Recursos Adicionales

- **Documentación FastAPI**: https://fastapi.tiangolo.com/
- **Documentación Pydantic**: https://pydantic-docs.helpmanual.io/
- **Documentación pytest**: https://docs.pytest.org/

---

¡Tu API de operaciones aritméticas está lista para usar! 🎉
