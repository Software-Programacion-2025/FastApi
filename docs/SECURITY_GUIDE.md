# 📖 Sistema de Seguridad - ToDo System

Este documento explica cómo funciona el sistema de autenticación y autorización implementado en el sistema de gestión de tareas.

## 🔐 CONFIGURACIÓN DE SEGURIDAD

### Rutas Públicas (No requieren autenticación):

- `/` - Página principal
- `/docs` - Documentación Swagger UI
- `/redoc` - Documentación ReDoc
- `/health` - Health check del sistema
- `/openapi.json` - Especificación OpenAPI

### Rutas con Métodos Públicos:

- `POST /users` - Registro de nuevos usuarios
- `POST /users/login` - Login de usuarios

### Rutas Solo Autenticación (sin permisos específicos):

- `GET /users/me` - Perfil del usuario actual

### Rutas Protegidas:

- Todas las demás rutas requieren:
  1. Token JWT válido en header Authorization: "Bearer `<token>`"
  2. Permisos específicos del rol para la ruta y método HTTP

## 🛡️ FLUJO DE AUTENTICACIÓN

1. **Registro**: POST /users (público)

   - Crea usuario con UUID, contraseña encriptada (bcrypt)
   - Asigna rol por defecto
   - Soporte para soft delete
2. **Login**: POST /users/login (público)

   - Verifica email y contraseña
   - Devuelve JWT token con user_id y rol_id
3. **Acceso a rutas protegidas**:

   - Middleware verifica token JWT
   - Normaliza rutas (UUID/números → {id})
   - Consulta permisos del rol en base de datos
   - Permite/deniega acceso según permisos

## 📋 CONFIGURACIÓN DE PERMISOS

Los permisos se configuran por:

- **Ruta**: URL normalizada (ej: /users/{id}, /tasks/{id}/state)
- **Método**: GET, POST, PUT, DELETE, PATCH
- **Rol**: admin, editor, viewer con permisos específicos

### Roles y Permisos del Sistema:

- **admin**: Acceso completo a users y tasks
- **editor**: Gestión de users y tasks (sin eliminar users)
- **viewer**: Solo lectura de tasks

## 🚀 CÓMO USAR EL SISTEMA

### Para desarrollo:

1. Ejecutar seeders: `python ./seeders/seed_main.py all`
2. Iniciar servidor: `uvicorn app:app --reload`
3. Login con usuario de prueba (admin / admin123)
4. Usar token en header Authorization

### Para Frontend:

1. POST /users/login con email/password
2. Guardar access_token del response
3. Enviar en todas las requests:
   Authorization: "Bearer <access_token>"

### Usuarios de Prueba:

- admin@todo.com / admin123 (Administrador)
- editor@todo.com / editor123 (Editor)
- viewer@todo.com / viewer123 (Viewer)

## ⚙️ VARIABLES DE ENTORNO

Configurar en .env:

```
SECRET_KEY=tu_clave_secreta_muy_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🔧 ADMINISTRACIÓN

- Los permisos se gestionan en la tabla `permisos`
- Las asignaciones rol-permiso en `rol_permiso`
- Los seeders cargan permisos básicos de CRUD para cada módulo

**El middleware AuthMiddleware está habilitado y protegiendo todas las rutas automáticamente.**
