from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from config.basemodel import Base
from config.cnx import engine

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
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=['*'],
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
