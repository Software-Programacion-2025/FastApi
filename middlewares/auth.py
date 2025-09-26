import bcrypt
import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import jwt
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', default='your secret key').encode('utf-8')

# Lista de rutas que no requieren autenticación
PUBLIC_ROUTES = [
    "/",
    "/home",
    "/test",
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/favicon.ico",
]

# Rutas que requieren métodos específicos sin autenticación
PUBLIC_METHODS = {
    "/users": ["POST"],  # Permitir registro de usuarios sin autenticación
    "/users/login": ["POST"],  # Permitir login sin autenticación
}

# Rutas que requieren autenticación pero no verificación de permisos específicos
AUTHENTICATED_ONLY_ROUTES = [
    "/users/me",  # Cualquier usuario autenticado puede ver su propio perfil
]


def hash_password(password: str) -> str:
    ''' Returns an encrypted string '''
    # Codifica la contraseña en bytes antes de hashearla
    password_bytes = password.encode('utf-8')
    # Utiliza la sal almacenada
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def compare_password(password:str, hashed_password: str):
    ''' Returns with passwords is correct '''
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30')))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=os.getenv('ALGORITHM', 'HS256'))
    return encoded_jwt

def verify_jwt_token(token: str) -> dict:
    """Verificar y decodificar un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[os.getenv('ALGORITHM', 'HS256')])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware de autenticación y autorización para verificar tokens JWT y permisos"""
    
    def __init__(self, app):
        super().__init__(app)
        # Importación lazy para evitar circular imports
        self._permission_service = None
    
    def get_permission_service(self):
        """Obtener servicio de permisos con lazy loading"""
        try:
            from config.cnx import SessionLocal
            from permisos.services import PermisoService
            db = SessionLocal()
            return PermisoService(db)
        except Exception as e:
            print(f"Error creating permission service: {e}")
            return None
    
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method
        
        # Verificar si la ruta es pública
        if self.is_public_route(path, method):
            response = await call_next(request)
            return response
        
        # Obtener el token del header Authorization
        authorization: Optional[str] = request.headers.get("Authorization")
        
        if not authorization:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token de autorización requerido"}
            )
        
        try:
            # Extraer el token (formato: "Bearer <token>")
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Esquema de autorización inválido. Use 'Bearer <token>'"}
                )
            
            # Verificar el token
            payload = verify_jwt_token(token)
            
            # Agregar información del usuario al request
            request.state.user = payload
            
            # Verificar permisos si está habilitado
            if self.should_check_permissions(path):
                user_role_id = payload.get('rol_id')
                if user_role_id:
                    # Normalizar la ruta para la verificación de permisos
                    normalized_path = self.normalize_path_for_permissions(path)
                    
                    try:
                        service = self.get_permission_service()
                        if service:
                            has_permission = service.user_has_permission(
                                user_role_id, 
                                normalized_path, 
                                method
                            )
                            
                            if not has_permission:
                                return JSONResponse(
                                    status_code=403,
                                    content={"detail": "No tiene permisos para acceder a este recurso"}
                                )
                        else:
                            print("Warning: Permission service not available, allowing access")
                    except Exception as permission_error:
                        # En caso de error con permisos, permitir acceso pero log el error
                        print(f"Error verificando permisos: {permission_error}")
            
        except ValueError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Formato de token inválido"}
            )
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
        except Exception as e:
            return JSONResponse(
                status_code=401,
                content={"detail": "Error de autenticación"}
            )
        
        response = await call_next(request)
        return response
    
    def is_public_route(self, path: str, method: str) -> bool:
        """Verificar si una ruta es pública"""
        # Verificar rutas completamente públicas
        if path in PUBLIC_ROUTES:
            return True
        
        # Verificar rutas con métodos específicos públicos
        if path in PUBLIC_METHODS:
            if method in PUBLIC_METHODS[path]:
                return True
        
        # Verificar rutas que empiecen con rutas públicas solo para prefijos bien conocidos (/docs, /redoc)
        # Evita que rutas como /users/* queden públicas por accidente
        prefix_whitelist = ["/docs", "/redoc"]
        for public_prefix in prefix_whitelist:
            if path.startswith(public_prefix):
                return True
        
        return False
    
    def should_check_permissions(self, path: str) -> bool:
        """Determinar si se debe verificar permisos para una ruta"""
        # No verificar permisos para rutas internas o de sistema
        skip_permission_paths = [
            "/health",
            "/favicon.ico",
            "/openapi.json",
            "/docs",
            "/redoc"
        ]
        
        for skip_path in skip_permission_paths:
            if path.startswith(skip_path):
                return False
        
        # No verificar permisos para rutas que solo requieren autenticación
        if path in AUTHENTICATED_ONLY_ROUTES:
            return False
        
        return True
    
    def normalize_path_for_permissions(self, path: str) -> str:
        """Normalizar ruta para verificación de permisos"""
        # Convertir rutas con IDs a formato de template
        # Ejemplo: /users/123 -> /users/{id}
        import re
        
        # Patrones actualizados para el nuevo sistema
        # IMPORTANTE: Los patrones más específicos deben ir primero
        patterns = [
            # Rutas UUID para users (ya que usa UUIDs) - PRIMERO para que se procesen antes que los números
            (r'/users/[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}/restore', '/users/{id}/restore'),
            (r'/users/[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}', '/users/{id}'),
            
            # Rutas de usuarios numéricas (migrado de usuarios -> users)
            (r'/users/\d+/restore', '/users/{id}/restore'),
            (r'/users/\d+', '/users/{id}'),
            
            # Rutas de tareas (nuevo módulo)
            (r'/tasks/\d+/state', '/tasks/{id}/state'),
            (r'/tasks/\d+/assign', '/tasks/{id}/assign'),
            (r'/tasks/\d+/unassign', '/tasks/{id}/unassign'),
            (r'/tasks/\d+', '/tasks/{id}'),
            
            # Rutas de roles (mantenidas)
            (r'/roles/\d+', '/roles/{id}'),
            
            # Rutas de permisos (mantenidas)
            (r'/permisos/rol/\d+', '/permisos/rol/{id}'),
            (r'/permisos/usuario/\d+/permisos', '/permisos/usuario/{id}/permisos'),
            (r'/permisos/ruta/[^/]+/metodo/[^/]+', '/permisos/ruta/{ruta}/metodo/{metodo}'),
            (r'/permisos/\d+', '/permisos/{id}'),
        ]
        
        normalized_path = path
        for pattern, replacement in patterns:
            normalized_path = re.sub(pattern, replacement, normalized_path)
        
        return normalized_path


### OAuth2 SCHEME PARA SWAGGER UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Dependency para verificar el token JWT en endpoints específicos
async def verify_token(token: str = Depends(oauth2_scheme)):
    """Verificar y decodificar el token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[os.getenv('ALGORITHM', 'HS256')])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"}
        )

# Dependency para obtener el usuario actual usando OAuth2
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Obtener el usuario actual desde el token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[os.getenv('ALGORITHM', 'HS256')])
        user_id = payload.get("user_id")
        email = payload.get("sub")
        
        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: datos de usuario faltantes",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return {
            "user_id": user_id,
            "sub": email,
            "roles": payload.get("roles", []),
            "permissions": payload.get("permissions", [])
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"}
        )

# Dependency para obtener el usuario actual desde el middleware (para compatibilidad)
async def get_current_user_from_middleware(request: Request):
    """Obtener el usuario actual desde el estado del request (middleware)"""
    if hasattr(request.state, 'user'):
        return request.state.user
    raise HTTPException(status_code=401, detail="Usuario no autenticado")