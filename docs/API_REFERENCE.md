# 📋 API Reference - ToDo System Backend

## 🚀 Base URL

```
http://localhost:5000
```

## 🔐 Autenticación

### Login (Público)

```http
POST /users/login
Content-Type: application/json

{
  "email": "admin@todo.com",
  "password": "admin123"
}
```

**Respuesta:**

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "admin@todo.com"
}
```

### Usar Token en Requests

```http
Authorization: Bearer <token>
```

## 📋 Endpoints por Módulo

### 👥 Usuarios (`/users`)

```http
GET    /users                 # Listar usuarios (requiere auth + permisos)
GET    /users/me              # Obtener perfil actual (requiere auth) 
GET    /users/{id}            # Obtener usuario por ID (requiere auth + permisos)
POST   /users                 # Crear usuario (público para registro)
POST   /users/login           # Login (público)
PUT    /users/{id}            # Actualizar usuario (requiere auth + permisos)
DELETE /users/{id}            # Eliminar usuario (soft delete, requiere auth + permisos)
PUT    /users/{id}/restore    # Restaurar usuario eliminado (requiere auth + permisos)
```

### 📝 Tareas (`/tasks`)

```http
GET    /tasks                 # Listar tareas (requiere auth)
GET    /tasks/{id}            # Obtener tarea por ID (requiere auth)
POST   /tasks                 # Crear tarea (requiere auth + permisos)
PUT    /tasks/{id}            # Actualizar tarea (requiere auth + permisos)
DELETE /tasks/{id}            # Eliminar tarea (requiere auth + permisos)
PUT    /tasks/{id}/state      # Cambiar estado de tarea (requiere auth + permisos)
POST   /tasks/{id}/assign     # Asignar usuario a tarea (requiere auth + permisos)
DELETE /tasks/{id}/unassign   # Desasignar usuario de tarea (requiere auth + permisos)
```

### 🛡️ Roles (`/roles`)

```http
GET    /roles                 # Listar roles (requiere auth)
GET    /roles/{id}            # Obtener rol por ID (requiere auth)  
POST   /roles                 # Crear rol (requiere auth + permisos)
PUT    /roles/{id}            # Actualizar rol (requiere auth + permisos)
DELETE /roles/{id}            # Eliminar rol (requiere auth + permisos)
```

### 🔐 Permisos (`/permisos`)

```http
GET    /permisos                                    # Listar permisos
GET    /permisos/{id}                               # Obtener permiso por ID
GET    /permisos/ruta/{ruta}/metodo/{metodo}        # Buscar por ruta y método
POST   /permisos                                    # Crear permiso
PUT    /permisos/{id}                               # Actualizar permiso  
DELETE /permisos/{id}                               # Eliminar permiso

# Gestión Rol-Permiso
POST   /permisos/rol/assign                         # Asignar permisos a rol
POST   /permisos/rol/remove                         # Remover permisos de rol
GET    /permisos/rol/{rol_id}                       # Ver permisos de un rol

# Verificación de Permisos
GET    /permisos/usuario/{user_rol_id}/permisos     # Permisos de usuario
POST   /permisos/usuario/verify                     # Verificar permiso específico
```

## 🚫 Endpoints Públicos (Sin Autenticación)

```
GET    /                  # Página principal
GET    /docs              # Documentación Swagger UI
GET    /redoc             # Documentación ReDoc
GET    /openapi.json      # Especificación OpenAPI
GET    /health            # Health check
POST   /users             # Registro de nuevos usuarios
POST   /users/login       # Login de usuarios
```

## 🔒 Flujo de Autenticación

1. **Registro**: `POST /users` con datos del usuario (email, password, name)
2. **Login**: `POST /users/login` con email/password
3. **Uso**: Incluir token en header: `Authorization: Bearer <token>`

## 📝 Formato de Respuestas

### Éxito (200/201)

```json
{
  "data": { /* objeto o array */ },
  "message": "Operación exitosa"
}
```

### Error (400/401/403/404/500)

```json
{
  "detail": "Descripción del error"
}
```

## 🧪 Ejemplos de Uso con curl

### Login

```bash
curl -X POST "http://localhost:5000/users/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@todo.com","password":"admin123"}'
```

### Consultar tareas protegidas

```bash
curl -X GET "http://localhost:5000/tasks" \
  -H "Authorization: Bearer <tu-token-aqui>"
```

### Crear tarea

```bash
curl -X POST "http://localhost:5000/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu-token-aqui>" \
  -d '{"title":"Nueva Tarea","description":"Descripción de la tarea","priority":"alta"}'
```

### Cambiar estado de tarea

```bash
curl -X PUT "http://localhost:5000/tasks/550e8400-e29b-41d4-a716-446655440000/state" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu-token-aqui>" \
  -d '{"status":"en_progreso"}'
```
