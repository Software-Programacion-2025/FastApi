# ✅ ToDo System - Backend API

Sistema completo de gestión de tareas desarrollado con **FastAPI** y **SQLAlchemy**. Proporciona una API REST robusta para administrar usuarios, tareas y permisos con autenticación JWT y sistema de autorización granular por roles.

## 🚀 Puesta en Marcha

### Prerrequisitos

- **Python 3.8+**
- **pip** (gestor de paquetes Python)
- **Git** para clonar el repositorio

### Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone <url-repositorio>
cd FastApi

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Cargar datos iniciales (usuarios, roles, tareas de prueba)
python ./seeders/seed_main.py

# 5. Iniciar el servidor
python app.py
```

### Verificación de Instalación

1. **Servidor ejecutándose**: [http://localhost:8000](http://localhost:8000)
2. **Documentación interactiva**: [http://localhost:8000/docs](http://localhost:8000/docs)
3. **Documentación alternativa**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🎯 Funcionalidades

### 🔐 Sistema de Autenticación y Autorización
- **Login/Registro** con JWT tokens
- **Roles por usuario**: Administrador, Gerente, Empleado, Cajero
- **Sistema de un rol por usuario** (simplificado y eficiente)
- **Middleware de autenticación** automático en rutas protegidas
- **Tokens JWT** con expiración configurable

### 👥 Gestión de Usuarios
- **CRUD completo** de usuarios con soft delete
- **Encriptación de contraseñas** con bcrypt
- **Perfiles de usuario** con información detallada
- **Asignación de roles** dinámicos
- **Restauración de usuarios** eliminados (soft delete)

### 📝 Sistema de Tareas Avanzado
- **Creación y edición** de tareas completas (título, descripción, estado)
- **Estados de tareas**: Pendiente, En Progreso, Completada
- **Asignación múltiple** de usuarios a tareas
- **Tareas por usuario** - cada usuario ve solo sus tareas asignadas
- **Gestión de asignaciones** - agregar/remover usuarios de tareas
- **Actualización de estados** independiente de la edición completa

### 🛡️ Seguridad y Middleware
- **Middleware personalizado** de autenticación JWT
- **Rutas públicas** configurables (login, registro, docs)
- **Verificación automática** de permisos por rol
- **Headers CORS** configurados para desarrollo
- **Logging configurado** sin verbosidad excesiva de SQLAlchemy

### 📊 Base de Datos y Modelos
- **SQLAlchemy ORM** con modelos relacionados
- **UUIDs** para identificación de usuarios
- **Timestamps automáticos** (created_at, updated_at)
- **Soft delete** para usuarios
- **Relaciones many-to-many** entre usuarios y tareas
- **Seeders modulares** para datos de pruebaem - Backend API

Sistema de gestión de tareas desarrollado con **FastAPI** y **SQLAlchemy**. Proporciona una API REST completa para administrar usuarios, tareas y permisos con autenticación JWT y sistema de autorización granular.

## 🎯 Funcionalidad Principal

**ToDo System Backend** es una API REST que permite gestionar:

- **👥 Usuarios**: Sistema completo de gestión de usuarios con autenticación JWT
- **📝 Tareas**: Creación, asignación y seguimiento de tareas con estados
- **�️ Roles y Permisos**: Control granular de acceso por ruta y método HTTP
- **� Seguridad**: Middleware de autenticación JWT con Bearer tokens
- **📊 Gestión de Estados**: Control de estados de tareas (pendiente, en progreso, completada)

## 🏗️ Arquitectura del Sistema

```
📁 ToDo-System/
├── 🚀 app.py                 # Aplicación principal FastAPI
├── 📊 todo_system.db        # Base de datos SQLite
├── 📋 requirements.txt      # Dependencias Python
├── 🔧 config/               # Configuración del sistema
│   ├── basemodel.py         # Modelo base SQLAlchemy
│   ├── cnx.py              # Conexión a base de datos
│   └── associations.py     # Tablas de relación (user_tasks, role_permissions)
├── 🛡️ middlewares/         # Middleware de seguridad
│   └── auth.py             # Autenticación JWT y permisos
├── 🌱 seeders/             # Datos iniciales (usuarios, roles, permisos, tareas)
├── 📁 users/               # Módulo de usuarios
│   ├── model.py            # Modelo User (UUID, soft delete)
│   ├── dto.py              # DTOs de usuarios
│   ├── services.py         # Lógica de negocio usuarios
│   └── routes.py           # API endpoints usuarios
├── 📁 tasks/               # Módulo de tareas
│   ├── model.py            # Modelo Task (estados, asignaciones)
│   ├── dto.py              # DTOs de tareas
│   ├── services.py         # Lógica de negocio tareas
│   └── routes.py           # API endpoints tareas
├── 📁 roles/               # Módulo de roles
├── 📁 permisos/            # Módulo de permisos
└── 📖 docs/                # Documentación completa
    ├── SECURITY_GUIDE.md   # Guía de seguridad y autenticación
    ├── API_REFERENCE.md    # Referencia completa de la API
    └── SWAGGER_GUIDE.md    # Guía de uso con Swagger UI
```

## 🚀 Inicio Rápido

> 👋 **¿Primera vez?** Te recomendamos la [**Guía de Swagger UI**](./SWAGGER_GUIDE.md) para empezar rápidamente sin instalaciones adicionales.

### Prerrequisitos

- Python 3.8+
- pip (gestor de paquetes Python)

### Instalación

1. **Clonar el repositorio**:

   ```bash
   git clone <url-repositorio>
   cd backend
   ```
2. **Crear entorno virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   ```
3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```
4. **Configurar variables de entorno**:

   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```
5. **Cargar datos iniciales**:

   ```bash
   python ./seeders/seed_main.py
   ```
6. **Iniciar el servidor**:

   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 5000
   ```
7. **Acceder a la documentación**:

   - Swagger UI: [http://localhost:5000/docs](http://localhost:5000/docs)
   - ReDoc: [http://localhost:5000/redoc](http://localhost:5000/redoc)

## 📚 Módulos del Sistema

| Módulo          | Descripción                               | Endpoints Principales                                                           |
|-----------------|-------------------------------------------|---------------------------------------------------------------------------------|
| **users**       | Gestión de usuarios y autenticación      | `GET /users`, `POST /users`, `POST /users/login`, `GET /users/me`              |
| **tasks**       | Sistema de gestión de tareas             | `GET /tasks`, `POST /tasks`, `PATCH /tasks/{id}`, `PUT /tasks/{id}/state`      |
| **roles**       | Administración de roles del sistema      | `GET /roles`, `POST /roles`, `PATCH /roles/{id}`                               |
| **permisos**    | Sistema de permisos granulares           | `GET /permisos`, `POST /permisos`, `POST /permisos/assign`                     |

## 🔐 Seguridad y Autenticación

El sistema incluye un **middleware de autenticación JWT** completo con:

- ✅ Encriptación de contraseñas (bcrypt)
- ✅ Tokens JWT con expiración configurable (30 minutos por defecto)
- ✅ Sistema de permisos por rol, ruta y método HTTP
- ✅ Rutas públicas configurables (login, registro)
- ✅ Verificación automática de permisos
- ✅ Bearer token authentication con Swagger UI integrado

### 🚀 Cómo Autenticarse

#### **Opción 1: Usando Swagger UI** (Recomendado para desarrollo)

1. **Abrir Swagger**: [http://localhost:5000/docs](http://localhost:5000/docs)
2. **Hacer login**:

   - Buscar el endpoint `POST /users/login`
   - Click en "Try it out"
   - Usar credenciales de prueba:
     ```json
     {
       "email": "admin@todo.com",
       "password": "admin123"
     }
     ```
   - Ejecutar y copiar el `token` de la respuesta
3. **Configurar autenticación**:

   - Click en el botón **"Authorize"** 🔒 (esquina superior derecha)
   - Pegar el token en el campo de valor
   - Click en "Authorize" y luego "Close"
4. **¡Listo!** Ahora puedes usar todos los endpoints protegidos

#### **Opción 2: Usando Postman**

1. **Login** - `POST http://localhost:5000/users/login`

   ```json
   {
     "email": "admin@todo.com", 
     "password": "admin123"
   }
   ```
2. **Copiar token** de la respuesta
3. **Configurar Authorization**:

   - Type: **Bearer Token**
   - Token: `<tu-token-aqui>`

### 🔑 Respuesta de Login

El endpoint de login retorna:

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": 1,
  "username": "admin"
}
```

### 📚 Guías de Uso Disponibles

- **🚀 [Guía de Swagger UI](./SWAGGER_GUIDE.md)** - Cómo usar la documentación interactiva
- **📮 [Guía de Postman](./POSTMAN_GUIDE.md)** - Configuración y uso con Postman
- **📋 [Referencia de API](./API_REFERENCE.md)** - Endpoints completos con ejemplos
- **🔒 [Guía de Seguridad](./SECURITY_GUIDE.md)** - Detalles técnicos de autenticación

## 🌱 Datos Iniciales (Seeders)

El sistema incluye seeders modulares para cargar datos de prueba:

- **Roles**: Administrador, Editor, Viewer
- **Usuarios**: Cuentas de prueba con UUIDs y contraseñas encriptadas
- **Permisos**: Control granular para módulos users y tasks
- **Tareas**: Ejemplos de tareas con diferentes estados y asignaciones

**📖 Para información sobre seeders, consulta: [`./seeders/README.md`](./seeders/README.md)**

## 🛠️ Tecnologías Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno y rápido
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: ORM para Python
- **[Pydantic](https://pydantic-docs.helpmanual.io/)**: Validación de datos
- **[JWT](https://jwt.io/)**: Autenticación con tokens
- **[bcrypt](https://pypi.org/project/bcrypt/)**: Encriptación de contraseñas
- **[SQLite](https://www.sqlite.org/)**: Base de datos ligera
- **[python-dotenv](https://pypi.org/project/python-dotenv/)**: Gestión de variables de entorno

## 🔧 Configuración

### Variables de Entorno (.env)

```env
# Seguridad JWT
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Base de datos (opcional para SQLite)
DATABASE_URL=sqlite:///./todo_system.db
```

### Estructura de Base de Datos

La base de datos incluye las siguientes tablas principales:

- `users` - Información de usuarios (UUID, soft delete, timestamps)
- `tasks` - Tareas del sistema (estados, asignaciones, fechas)
- `roles` - Roles disponibles (Administrador, Editor, Viewer)
- `permisos` - Permisos granulares por ruta y método
- `rol_permiso` - Tabla intermedia rol-permiso (many-to-many)
- `user_task_association` - Tabla intermedia user-task (many-to-many)

## 🧪 Testing y Desarrollo

### Usuarios de Prueba (después de ejecutar seeders)

| Email             | Contraseña | Rol           | Descripción                    |
|-------------------|------------|---------------|--------------------------------|
| admin@todo.com    | admin123   | Administrador | Acceso completo al sistema     |
| editor@todo.com   | editor123  | Editor        | Gestión de usuarios y tareas   |
| viewer@todo.com   | viewer123  | Viewer        | Solo lectura de tareas         |

### Comandos Útiles

```bash
# Ejecutar seeders completos
python ./seeders/seed_main.py

# Ejecutar seeder específico
python ./seeders/seed_roles.py

# Iniciar con recarga automática
uvicorn app:app --reload --host 0.0.0.0 --port 5000

# Ver documentación
curl http://localhost:5000/docs
```

### Características Técnicas

- ✅ **Modularidad** - Cada entidad tiene su propio módulo (model, dto, service, routes)
- ✅ **Seguridad JWT** - Tokens con expiración y roles/permisos granulares
- ✅ **Middleware personalizado** - Autenticación automática en rutas protegidas
- ✅ **Seeders organizados** - Datos de prueba modulares y reutilizables
- ✅ **Documentación automática** - Swagger UI y ReDoc incluidos
- ✅ **Validaciones** - DTOs con Pydantic
- ✅ **Manejo de errores** - Responses HTTP consistentes

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

**MIT License**

Este proyecto es desarrollado para fines educativos como parte del sistema **ToDo System**.

### Términos de Uso

- ✅ **Uso libre** para fines educativos y de aprendizaje
- ✅ **Modificación y distribución** permitida con atribución
- ✅ **Uso comercial** permitido bajo los términos de la licencia MIT
- ⚠️ **Sin garantía** - el software se proporciona "tal como está"

### Atribución

Si utilizas este proyecto como base para tu propio desarrollo, se agradece la atribución al proyecto original.

```
ToDo System API - Sistema de gestión de tareas con FastAPI
Desarrollado como proyecto educativo
```

---

**🚀 ¡Tu API REST de gestión de tareas está lista para usar!**
