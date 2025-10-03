from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from config.basemodel import Base
from config.cnx import engine

# === CONFIGURACIÓN DE LOGGING COMPLETAMENTE SILENCIOSO ===
import logging

# Remover todos los handlers existentes del root logger
root_logger = logging.getLogger()
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Configurar logging básico solo para CRITICAL
logging.basicConfig(
    level=logging.CRITICAL,
    format='%(levelname)s: %(message)s',
    force=True  # Forzar reconfiguración
)

# Lista completa de loggers de SQLAlchemy para silenciar
sqlalchemy_loggers = [
    'sqlalchemy', 'sqlalchemy.engine', 'sqlalchemy.engine.Engine', 
    'sqlalchemy.pool', 'sqlalchemy.pool.impl', 'sqlalchemy.dialects',
    'sqlalchemy.orm', 'sqlalchemy.orm.strategies'
]

# Silenciar completamente SQLAlchemy
for logger_name in sqlalchemy_loggers:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

# Silenciar otros componentes de la aplicación
app_loggers = [
    'uvicorn', 'uvicorn.access', 'uvicorn.error', 'fastapi',
    'users', 'users.services', 'users.routes',
    'tasks', 'tasks.services', 'tasks.routes',
    'roles', 'roles.services', 'permisos'
]

for logger_name in app_loggers:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

app_logger = logging.getLogger('app')

# Importar todos los modelos para asegurar que se registren en Base.metadata
from roles.model import Rol
from permisos.model import Permiso
from users.model import User
from tasks.model import Task
from config.associations import rol_permiso_association, user_task_association

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# Importamos las rutas de los diferentes modelos 
from default.routes import default
from middlewares.auth import AuthMiddleware
from roles.routes import roles
from users.routes import users
from tasks.routes import tasks
from permisos.routes import router as permisos_router

app = FastAPI(
    title="ToDo System API",
    description="API REST para gestión de usuarios y tareas con autenticación JWT y permisos granulares",
    version="1.0"
)

# Asignamos los Middleware para los CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Cambia esto según el origen de tu frontend
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],  # Permitir todos los headers incluyendo Authorization
    allow_credentials=True,
)
# Agregamos el middleware de autenticación
app.add_middleware(AuthMiddleware)

#Routas de la API
app.include_router(default, prefix='', tags=['Rutas por Default'])

app.include_router(roles, prefix="/roles", tags=["Roles"])
app.include_router(users, prefix="/users", tags=["Users"])
app.include_router(tasks, prefix="/tasks", tags=["Tasks"])
app.include_router(permisos_router, prefix="/permisos", tags=["Permisos"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ToDo System API",
        version="1.0",
        description="API REST para gestión de usuarios y tareas con autenticación JWT y permisos granulares",
        routes=app.routes,
    )
    
    # Configurar el esquema de seguridad personalizado para JWT Bearer
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Ingresa tu token JWT obtenido del endpoint /users/login"
        }
    }
    
    # Rutas que no requieren autenticación
    public_routes = [
        "/",
        "/home", 
        "/test",
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/favicon.ico"
    ]
    
    # Rutas con métodos específicos públicos
    public_methods = {
        "/users": ["post"],  # Registro de usuarios
        "/users/login": ["post"]  # Login
    }
    
    # Agregar seguridad a todas las rutas excepto las públicas
    if "paths" in openapi_schema:
        for path, methods in openapi_schema["paths"].items():
            for method, details in methods.items():
                # Verificar si la ruta es pública
                is_public = False
                
                # Verificar rutas completamente públicas
                if path in public_routes:
                    is_public = True
                
                # Verificar métodos específicos públicos
                if path in public_methods and method.lower() in public_methods[path]:
                    is_public = True
                
                # Si no es pública, agregar seguridad
                if not is_public:
                    if "security" not in details:
                        details["security"] = [{"HTTPBearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Solo mostrar mensaje de inicio si es necesario
    if os.getenv('SHOW_STARTUP', 'true').lower() == 'true':
        print("🚀 FastAPI Server - http://localhost:8000")
        
    uvicorn.run(
        "app:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="critical",  # Solo errores críticos
        access_log=False,     # Sin access logs
        server_header=False,  # Sin headers del servidor
        date_header=False     # Sin fecha en headers
    )