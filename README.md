# 🚀 FastApi

**Proyecto de Ejemplo con FastApi, SQLAlchemy 2.0, Alembic y Sistema de Validaciones Robusto**

Este proyecto implementa una API RESTful completa con FastAPI, incluyendo gestión de usuarios y tareas, migraciones de base de datos, validaciones exhaustivas y manejo de errores profesional.

---

## 📋 Tabla de Contenidos

- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [⚡ Servidor de Desarrollo](#-servidor-de-desarrollo)
- [� Sistema de Autenticación](#-sistema-de-autenticación)
- [�🗂️ Migraciones con Alembic](#️-migraciones-con-alembic)
- [🌱 Seeders](#-seeders)
- [🛡️ Sistema de Validaciones](#️-sistema-de-validaciones)
- [📊 Monitoreo y Logging](#-monitoreo-y-logging)
- [🚨 Manejo de Errores](#-manejo-de-errores)
- [📚 Documentación Técnica](#-documentación-técnica)

---

## 📁 Estructura del Proyecto

```text
FastApi/
├── alembic.ini                 # Configuración de Alembic
├── app.py                     # Aplicación principal FastAPI
├── mibase.db                  # Base de datos SQLite
├── requirements.txt           # Dependencias del proyecto
├── seed.py                    # Seeder para datos de prueba
├── ERROR_HANDLING.md          # Documentación de manejo de errores
├── SERVICES_VALIDATION.md     # Documentación de validaciones
├── alembic/
│   ├── env.py                # Configuración de entorno Alembic
│   └── versions/             # Archivos de migración
├── config/
│   ├── basemodel.py          # Modelo base SQLAlchemy
│   └── cnx.py               # Configuración de conexión BD
├── default/
│   └── routes.py            # Rutas por defecto y health check
├── middlewares/
│   └── auth.py              # Middleware de autenticación
├── tasks/
│   ├── dto.py              # DTOs para tareas
│   ├── model.py            # Modelo de tarea SQLAlchemy
│   ├── routes.py           # Endpoints de tareas
│   └── services.py         # Lógica de negocio de tareas
└── users/
    ├── dto.py              # DTOs para usuarios
    ├── model.py            # Modelo de usuario SQLAlchemy
    ├── ruotes.py           # Endpoints de usuarios
    └── services.py         # Lógica de negocio de usuarios
```

---

## ⚡ Servidor de Desarrollo

Para iniciar el servidor de desarrollo ejecuta:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Endpoints Disponibles

- **Documentación Swagger**: `http://localhost:8000/docs`
- **Documentación ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

### Características del Servidor

- ✅ Recarga automática en modo desarrollo
- ✅ CORS configurado para desarrollo
- ✅ Documentación OpenAPI automática
- ✅ Validaciones exhaustivas en todos los endpoints
- ✅ Manejo robusto de errores HTTP
- ✅ **Middleware de autenticación JWT integrado**

---

## 🔐 Sistema de Autenticación

El proyecto implementa autenticación JWT (JSON Web Tokens) con middleware personalizado para proteger las rutas de la API.

### Configuración de Variables de Entorno

Copia el archivo `.env.example` a `.env` y configura las variables:

```bash
cp .env.example .env
```

Variables importantes para autenticación:
```bash
SECRET_KEY=your_super_secret_key_here_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Middleware de Autenticación

#### Rutas Públicas (No requieren token)
- ✅ `/` - Página de inicio
- ✅ `/docs` - Documentación Swagger
- ✅ `/health` - Health check
- ✅ `POST /users` - Registro de usuarios
- ✅ `POST /users/login` - Login de usuarios

#### Rutas Protegidas (Requieren token JWT)
- 🔒 `GET /users` - Listar usuarios
- 🔒 `GET /users/{id}` - Obtener usuario específico
- 🔒 `GET /users/me` - Información del usuario autenticado
- 🔒 `PUT /users/{id}` - Actualizar usuario
- 🔒 `DELETE /users/{id}` - Eliminar usuario
- 🔒 Todas las rutas de `/tasks`

### Uso de la Autenticación

#### 1. Registro de Usuario
```bash
POST /users
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Doe",
  "emails": "john.doe@example.com",
  "ages": 30,
  "password": "securePassword123"
}
```

#### 2. Login y Obtención de Token
```bash
POST /users/login
Content-Type: application/json

{
  "emails": "john.doe@example.com",
  "password": "securePassword123"
}
```

**Respuesta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "firstName": "John",
    "lastName": "Doe",
    "emails": "john.doe@example.com",
    "ages": 30,
    "tasks": []
  }
}
```

#### 3. Usar Token en Requests Protegidos
```bash
GET /users/me
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Características del Sistema de Autenticación

- ✅ **JWT Tokens**: Tokens seguros con expiración configurable
- ✅ **Middleware Global**: Protección automática de rutas
- ✅ **Rutas Públicas**: Configuración flexible de endpoints públicos
- ✅ **Validación de Tokens**: Verificación automática de tokens válidos
- ✅ **Información de Usuario**: Acceso a datos del usuario autenticado
- ✅ **Manejo de Errores**: Respuestas HTTP apropiadas para errores de auth

---

## 🗂️ Migraciones con Alembic

Para iniciar el servidor de desarrollo ejecuta:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Endpoints Disponibles

- **Documentación Swagger**: `http://localhost:8000/docs`
- **Documentación ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

### Características del Servidor

- ✅ Recarga automática en modo desarrollo
- ✅ CORS configurado para desarrollo
- ✅ Documentación OpenAPI automática
- ✅ Validaciones exhaustivas en todos los endpoints
- ✅ Manejo robusto de errores HTTP

---

## 🗂️ Migraciones con Alembic

Alembic se utiliza para gestionar las migraciones de la base de datos con soporte completo para SQLAlchemy 2.0.

### 🛠️ Configuración Inicial

```bash
pip install alembic
alembic init alembic
```

### ⚙️ Configuración de Base de Datos

1. **Configura la URL** en `alembic.ini`:
   ```ini
   sqlalchemy.url = sqlite:///mibase.db
   ```

2. **Registra los modelos** en `alembic/env.py`:
   ```python
   from config.basemodel import Base
   from users import model as users_model
   from tasks import model as tasks_model
   target_metadata = Base.metadata
   ```

### 📝 Comandos de Migración

```bash
# Generar migración automática
alembic revision --autogenerate -m "descripción de la migración"

# Aplicar migraciones
alembic upgrade head

# Ver historial de migraciones
alembic history

# Revertir una migración
alembic downgrade -1
```

---

## 🌱 Seeders

Sistema de población de datos usando Typer CLI para generar datos de prueba realistas.

### Instalación de Dependencias

```bash
pip install typer faker
```

### Uso del Seeder

```bash
# Crear 10 usuarios por defecto
python seed.py

# Crear cantidad específica de usuarios
python seed.py --count 25

# Ver ayuda
python seed.py --help
```

### Características del Seeder

- ✅ Datos realistas generados con Faker
- ✅ Validación de unicidad de emails
- ✅ Contraseñas hasheadas automáticamente
- ✅ CLI intuitivo con Typer
- ✅ Logging de progreso y resultados

---

## 🛡️ Sistema de Validaciones

### Validaciones a Nivel de Rutas

#### Validaciones de Tareas
- **ID de tarea**: Números positivos únicamente
- **Título**: Campo requerido y no vacío
- **Estado**: Validación contra valores permitidos (`pending`, `in_progress`, `completed`, `cancelled`)
- **Asignación de usuarios**: Verificación de existencia y prevención de duplicados

#### Validaciones de Usuarios
- **UUID**: Formato válido de identificadores únicos
- **Email**: Formato RFC 5322 con expresiones regulares
- **Campos requeridos**: firstName, lastName, emails obligatorios
- **Edad**: Rango válido (1-150 años)
- **Contraseña**: Longitud mínima de 6 caracteres

### Validaciones a Nivel de Servicios

#### Características Implementadas
- ✅ **Validación de entrada exhaustiva** en todos los parámetros
- ✅ **Verificación de integridad referencial** (FK, usuarios activos)
- ✅ **Prevención de duplicados** (emails únicos, asignaciones repetidas)
- ✅ **Normalización de datos** (trim, lowercase en emails)
- ✅ **Transacciones seguras** con rollback automático
- ✅ **Gestión de recursos** con cierre garantizado de sesiones

---

## 📊 Monitoreo y Logging

### Sistema de Logging Integrado

```python
# Configuración automática en servicios
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

#### Tipos de Logs Generados

- **INFO**: Operaciones exitosas con estadísticas
- **WARNING**: Intentos de operaciones inválidas
- **ERROR**: Errores de sistema y base de datos

#### Información Registrada

- ✅ **Operaciones CRUD**: Creación, actualización, eliminación exitosas
- ✅ **Intentos fallidos**: IDs no encontrados, validaciones fallidas
- ✅ **Estadísticas**: Cantidad de registros procesados
- ✅ **Cambios de estado**: Tracking de modificaciones importantes
- ✅ **Errores técnicos**: Detalles para debugging y monitoreo

---

## 🚨 Manejo de Errores

### Códigos de Estado HTTP Estandarizados

| Código | Uso | Descripción |
|--------|-----|-------------|
| **200** | `HTTP_200_OK` | Operaciones exitosas |
| **201** | `HTTP_201_CREATED` | Recursos creados |
| **400** | `HTTP_400_BAD_REQUEST` | Validaciones fallidas |
| **404** | `HTTP_404_NOT_FOUND` | Recursos no encontrados |
| **409** | `HTTP_409_CONFLICT` | Conflictos de integridad |
| **500** | `HTTP_500_INTERNAL_SERVER_ERROR` | Errores internos |

### Jerarquía de Manejo de Excepciones

1. **HTTPException**: Re-lanzamiento con código original
2. **ValueError**: Errores de validación y lógica (400/404)
3. **IntegrityError**: Conflictos de BD (409)
4. **SQLAlchemyError**: Errores generales de BD (500)
5. **Exception**: Errores inesperados (500)

### Ejemplos de Respuestas de Error

```json
// Error 400 - Validación
{
  "detail": "El título de la tarea es requerido"
}

// Error 404 - No encontrado
{
  "detail": "Usuario con ID 123e4567-e89b-12d3-a456-426614174000 no encontrado"
}

// Error 409 - Conflicto
{
  "detail": "Email ya está registrado"
}
```

---

## 📚 Documentación Técnica

### Documentos Disponibles

- **[ERROR_HANDLING.md](./ERROR_HANDLING.md)**: Guía completa de manejo de errores HTTP
- **[SERVICES_VALIDATION.md](./SERVICES_VALIDATION.md)**: Documentación de validaciones en servicios

### Características Técnicas del Proyecto

#### Base de Datos
- ✅ **SQLAlchemy 2.0** con sintaxis moderna
- ✅ **SQLite** para desarrollo (fácil migración a PostgreSQL/MySQL)
- ✅ **Migraciones automáticas** con Alembic
- ✅ **Relaciones many-to-many** entre usuarios y tareas
- ✅ **Soft delete** para preservar datos históricos

#### API Features
- ✅ **OpenAPI 3.0** con ejemplos en todos los DTOs
- ✅ **Pydantic v2** para validación y serialización
- ✅ **CORS** configurado para desarrollo
- ✅ **Health check** para monitoreo
- ✅ **Gestión de estados** de tareas
- ✅ **Asignación múltiple** de usuarios a tareas

#### Desarrollo y Calidad
- ✅ **Type hints** completos con TYPE_CHECKING
- ✅ **Estructura modular** por funcionalidad
- ✅ **Separación de responsabilidades** (routes/services/models)
- ✅ **Error handling** profesional en todas las capas
- ✅ **Logging** estructurado para debugging
- ✅ **Documentación** exhaustiva y mantenida

### Requisitos del Sistema

```bash
# Python 3.8+
pip install -r requirements.txt
```

**Dependencias principales:**
- FastAPI 0.115+
- SQLAlchemy 2.0+
- Alembic 1.16+
- Pydantic 2.11+
- Typer 0.16+
- Faker 37.5+

---

---
