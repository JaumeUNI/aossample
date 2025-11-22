# Interfaz Gráfica - Sistema de Gestión de Rutinas Deportivas

## 📋 Descripción

Esta interfaz gráfica web permite interactuar con todas las funcionalidades básicas de la API de gestión de rutinas deportivas de forma visual e intuitiva.

## 🚀 Cómo Usar

### 1. Iniciar el Servidor API

Primero, asegúrate de que el servidor FastAPI esté ejecutándose:

```bash
# Activar el entorno virtual (Windows)
venv\Scripts\activate

# Ejecutar el servidor
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

El servidor estará disponible en `http://127.0.0.1:8000`

### 2. Abrir la Interfaz Gráfica

Simplemente abre el archivo `index.html` en tu navegador web. Puedes hacerlo de dos formas:

**Opción 1: Doble clic**
- Navega hasta el archivo `index.html` en el explorador de archivos
- Haz doble clic para abrirlo en tu navegador predeterminado

**Opción 2: Desde la línea de comandos**
```bash
# En Windows
start index.html

# O simplemente arrastra el archivo al navegador
```

### 3. Usar la Interfaz

La interfaz está organizada en pestañas:

#### 🏋️ **Ejercicios**
- **Crear ejercicio**: Haz clic en "➕ Nuevo Ejercicio" y completa el formulario
- **Filtrar ejercicios**: Usa los filtros por tipo, dificultad y grupo muscular
- **Ver ejercicios**: Todos los ejercicios se muestran en tarjetas con su información completa
- **Eliminar ejercicio**: Usa el botón "Eliminar" en cada tarjeta

#### 🏃 **Rutinas**
- **Crear rutina**: Haz clic en "➕ Nueva Rutina" y completa el formulario
- **Ver rutinas**: Todas las rutinas se muestran con sus detalles
- **Eliminar rutina**: Usa el botón "Eliminar" en cada tarjeta

#### 👤 **Usuarios**
- **Registrar usuario**: Haz clic en "➕ Nuevo Usuario" y completa el formulario
- **Ver usuarios**: Todos los usuarios registrados se muestran con su información
- **Eliminar usuario**: Usa el botón "Eliminar" en cada tarjeta

#### 🏋️ **Sesiones**
- **Iniciar sesión**: Haz clic en "➕ Nueva Sesión" e ingresa el ID del usuario y la rutina
- **Ver sesiones**: Todas las sesiones de entrenamiento se muestran con su estado

#### 📈 **Progreso**
- **Registrar progreso**: Haz clic en "➕ Registrar Progreso" y completa el formulario
- **Ver progreso**: Todos los registros de progreso se muestran con sus detalles

## 🎨 Características de la Interfaz

- **Diseño moderno**: Interfaz con gradientes y animaciones suaves
- **Responsive**: Se adapta a diferentes tamaños de pantalla
- **Navegación por pestañas**: Fácil acceso a todas las funcionalidades
- **Formularios intuitivos**: Campos claramente etiquetados y validados
- **Visualización en tarjetas**: Información organizada y fácil de leer
- **Filtros avanzados**: Para ejercicios, puedes filtrar por tipo, dificultad y grupo muscular
- **Feedback visual**: Mensajes de éxito y error claros

## 🔧 Configuración

Si necesitas cambiar la URL de la API (por ejemplo, si el servidor está en otro puerto), edita la constante `API_BASE_URL` en el archivo `app.js`:

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000';  // Cambia aquí si es necesario
```

## 📝 Notas Importantes

1. **CORS habilitado**: La API ahora tiene CORS habilitado para permitir peticiones desde el navegador
2. **Datos en memoria**: Los datos se almacenan en memoria, por lo que se perderán al reiniciar el servidor
3. **Navegador compatible**: Funciona en todos los navegadores modernos (Chrome, Firefox, Edge, Safari)

## 🐛 Solución de Problemas

### La interfaz no carga los datos
- Verifica que el servidor FastAPI esté ejecutándose
- Abre la consola del navegador (F12) para ver errores
- Verifica que la URL de la API sea correcta en `app.js`

### Error de CORS
- Asegúrate de que el archivo `app/main.py` tenga la configuración de CORS (ya está incluida)
- Reinicia el servidor después de cualquier cambio

### Los formularios no funcionan
- Verifica que todos los campos requeridos estén completos
- Revisa la consola del navegador para ver mensajes de error
- Asegúrate de que el servidor esté respondiendo correctamente

## 📚 Funcionalidades Implementadas

✅ CRUD completo de Ejercicios
✅ CRUD completo de Rutinas
✅ CRUD completo de Usuarios
✅ Crear y visualizar Sesiones de Entrenamiento
✅ Crear y visualizar Progreso del Usuario
✅ Filtros para Ejercicios
✅ Interfaz responsive y moderna
✅ Validación de formularios
✅ Mensajes de feedback al usuario

---

¡Disfruta usando la interfaz gráfica! 🎉

