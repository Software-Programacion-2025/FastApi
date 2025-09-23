# 🚀 Guía de Uso con Swagger UI - ToDo System API

Esta guía te explica cómo usar la **documentación interactiva Swagger** de la API del sistema ToDo.

## 🎯 Acceso Rápido

**URL de Swagger**: <http://localhost:5000/docs>

> **Nota**: Asegúrate de que el servidor esté corriendo antes de acceder a Swagger UI.

## 🔐 Autenticación en Swagger

### Paso 1: Hacer Login

1. **Encuentra el endpoint de login**:
   - Busca la sección **"Users"**
   - Localiza `POST /users/login`

2. **Probar el login**:
   - Click en `POST /users/login`
   - Click en **"Try it out"**
   - En el campo Request body, usa:
   ```json
   {
     "email": "admin@todo.com",
     "password": "admin123"
   }
   ```
   - Click en **"Execute"**

3. **Copiar el token**:
   - En la respuesta, copia el valor del campo `token`
   - Debería verse así: `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...`

### Paso 2: Configurar Autorización

1. **Buscar el botón Authorize**:
   - En la esquina superior derecha de Swagger UI
   - Click en el botón **"Authorize"** 🔒

2. **Configurar Bearer Token**:
   - Se abrirá un modal de autorización
   - En el campo **"Value"** pega tu token
   - **NO** agregues "Bearer " al inicio, solo pega el token
   - Click en **"Authorize"**
   - Click en **"Close"**

3. **¡Listo!**:
   - Ahora verás un candado cerrado 🔒 en los endpoints protegidos
   - Todos los requests incluirán automáticamente tu token

## 👥 Usuarios de Prueba

| Email            | Contraseña  | Rol           | Permisos                        |
|------------------|-------------|---------------|---------------------------------|
| admin@todo.com   | admin123    | Administrador | ✅ Acceso completo              |
| editor@todo.com  | editor123   | Editor        | ✅ Gestión users y tasks        |
| viewer@todo.com  | viewer123   | Viewer        | ⚠️ Solo lectura de tareas       |

## 📋 Navegación por Módulos

### 🏠 Default
- Información básica del sistema
- Health check

### 👥 Users (Usuarios)
- **`POST /users/login`** - 🟢 Público - Login del sistema
- **`GET /users`** - 🔒 Protegido - Listar usuarios
- **`GET /users/me`** - 🔒 Protegido - Mi perfil
- **`POST /users`** - 🟢 Público - Registro de usuario
- **`PUT /users/{id}`** - 🔒 Protegido - Actualizar usuario
- **`DELETE /users/{id}`** - 🔒 Protegido - Eliminar usuario (soft delete)
- **`PUT /users/{id}/restore`** - 🔒 Protegido - Restaurar usuario eliminado

### 📝 Tasks (Tareas)
- **`GET /tasks`** - 🔒 Protegido - Listar tareas
- **`GET /tasks/{id}`** - 🔒 Protegido - Obtener tarea por ID
- **`POST /tasks`** - 🔒 Protegido - Crear nueva tarea
- **`PUT /tasks/{id}`** - 🔒 Protegido - Actualizar tarea
- **`DELETE /tasks/{id}`** - 🔒 Protegido - Eliminar tarea
- **`PUT /tasks/{id}/state`** - 🔒 Protegido - Cambiar estado de tarea
- **`POST /tasks/{id}/assign`** - 🔒 Protegido - Asignar usuario a tarea
- **`DELETE /tasks/{id}/unassign`** - 🔒 Protegido - Desasignar usuario de tarea

### 🛡️ Roles
- **`GET /roles`** - 🔒 Protegido - Listar roles
- **`POST /roles`** - 🔒 Protegido - Crear rol
- **`PUT /roles/{id}`** - 🔒 Protegido - Actualizar rol
- **`DELETE /roles/{id}`** - 🔒 Protegido - Eliminar rol

### 🔐 Permisos (Nuevo!)
- **`GET /permisos`** - 🔒 Protegido - Listar permisos
- **`POST /permisos`** - 🔒 Protegido - Crear permiso
- **`GET /permisos/{id}`** - 🔒 Protegido - Obtener permiso
- **`PUT /permisos/{id}`** - 🔒 Protegido - Actualizar permiso
- **`DELETE /permisos/{id}`** - 🔒 Protegido - Eliminar permiso

#### Gestión Avanzada de Permisos:
- **`POST /permisos/rol/assign`** - Asignar permisos a rol
- **`POST /permisos/rol/remove`** - Remover permisos de rol
- **`GET /permisos/rol/{rol_id}`** - Ver permisos de un rol
- **`GET /permisos/usuario/{user_rol_id}/permisos`** - Permisos de usuario
- **`POST /permisos/usuario/verify`** - Verificar permiso específico

## 🎯 Ejemplos Prácticos

### 1. Primer Login y Exploración

1. **Login** con `admin@todo.com/admin123`
2. **Autorizar** en Swagger con el token obtenido
3. **Probar** `GET /users/me` para ver tu perfil
4. **Explorar** `GET /users` para ver todos los usuarios
5. **Listar tareas**: `GET /tasks` para ver las tareas del sistema

### 2. Gestión de Tareas

1. **Ver tareas disponibles**: `GET /tasks`
2. **Crear nueva tarea**: `POST /tasks`
   ```json
   {
     "title": "Mi nueva tarea",
     "description": "Descripción detallada",
     "priority": "alta",
     "status": "pendiente"
   }
   ```
3. **Cambiar estado de tarea**: `PUT /tasks/{id}/state`
4. **Asignar tarea a usuario**: `POST /tasks/{id}/assign`

### 3. Gestión de Usuarios (solo admin/editor)

1. **Listar usuarios**: `GET /users`
2. **Crear usuario nuevo**: `POST /users`
3. **Actualizar usuario**: `PUT /users/{id}`
4. **Eliminar usuario** (soft delete): `DELETE /users/{id}`
5. **Restaurar usuario**: `PUT /users/{id}/restore`

## 🔄 Refrescar Token

Si tu sesión expira (después de 30 minutos):

1. **Repetir el proceso de login**
2. **Actualizar la autorización** con el nuevo token
3. **Continuar usando la API**

## 💡 Tips y Trucos

### ✅ Buenas Prácticas
- **Usar admin** para probar todas las funcionalidades
- **Copiar ejemplos** de Request/Response para entender la estructura
- **Leer las descripciones** de cada endpoint
- **Probar con diferentes roles** para entender el sistema de permisos

### ⚠️ Errores Comunes
- **Token no configurado**: Error 401 - Configurar autorización
- **Permisos insuficientes**: Error 403 - Usar usuario con más permisos  
- **Token expirado**: Error 401 - Hacer login nuevamente
- **Datos inválidos**: Error 422 - Revisar el formato del Request Body

### 🚀 Funcionalidades Avanzadas
- **Filtros y paginación**: Disponibles en endpoints de listado
- **Búsqueda específica**: Algunos endpoints permiten filtros
- **Responses detallados**: Incluyen códigos de error específicos
- **Validación automática**: Swagger valida los datos antes de enviar

## 📊 Códigos de Respuesta

| Código | Significado | Cuándo Aparece |
| ------ | ----------- | -------------- |
| 200    | ✅ OK | Operación exitosa |
| 201    | ✅ Creado | Recurso creado exitosamente |
| 400    | ❌ Bad Request | Datos inválidos en el request |
| 401    | 🔒 Unauthorized | Token inválido o faltante |
| 403    | 🚫 Forbidden | Sin permisos para el recurso |
| 404    | 🔍 Not Found | Recurso no encontrado |
| 422    | ⚠️ Validation Error | Error de validación de datos |
| 500    | 💥 Server Error | Error interno del servidor |

## 🔗 Recursos Adicionales

- **Documentación Completa**: [`README.md`](./README.md)
- **Guía de Postman**: [`POSTMAN_GUIDE.md`](./POSTMAN_GUIDE.md)  
- **Referencia de API**: [`API_REFERENCE.md`](./API_REFERENCE.md)
- **Guía de Seguridad**: [`SECURITY_GUIDE.md`](./SECURITY_GUIDE.md)

---

**🎉 ¡Swagger UI te permite probar toda la API sin escribir código!**

> **Próximos pasos**: Una vez que domines Swagger, puedes usar la [Guía de Postman](./POSTMAN_GUIDE.md) para automatizar tests y crear collections reutilizables.