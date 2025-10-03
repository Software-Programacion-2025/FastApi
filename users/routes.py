from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import List
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .dto import UserCreate, UserOut, UserUpdate, UserLogin, Token, UserInsert, UserSimple, RoleAssignment
from .services import (
    get_all_users, get_all_users_deleted, get_users_simple, get_user_by_id, 
    create_user, insert_user, update_user, 
    soft_delete_user, restore_user, login_user,
    assign_role, remove_role
)
from middlewares.auth import get_current_user
from middlewares.security import get_current_user_token
import time
import logging

# Configurar logger para este módulo
logger = logging.getLogger(__name__)

# Dependency personalizado para logging de operaciones sensibles
async def log_sensitive_operation(request: Request, current_user: dict = Depends(get_current_user)):
    """Middleware/dependency para operaciones sensibles de usuarios"""
    start_time = time.time()
    
    # Log de la operación
    operation = f"{request.method} {request.url.path}"
    
    return {
        "user_id": current_user["user_id"],
        "user_email": current_user["sub"], 
        "operation": operation,
        "start_time": start_time
    }

# Dependency para logging de operaciones de lectura
async def log_read_operation(request: Request):
    """Middleware/dependency simple para operaciones de lectura"""
    start_time = time.time()
    operation = f"{request.method} {request.url.path}"
    
    return {
        "operation": operation,
        "start_time": start_time
    }

users = APIRouter()

@users.get('', response_model=List[UserOut], status_code=status.HTTP_200_OK)
def get_users(log_info: dict = Depends(log_read_operation)):
    """Obtener todos los usuarios activos - CON middleware de lectura"""
    try:
        return get_all_users()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener los usuarios"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener los usuarios"
        )

@users.get('/simple', response_model=List[UserSimple], status_code=status.HTTP_200_OK)
def get_users_simple_list(current_user: dict = Depends(get_current_user_token)):
    """Obtener lista simplificada de usuarios para selectors - Requiere autenticación"""
    try:
        return get_users_simple()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener la lista de usuarios"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener la lista de usuarios"
        )

@users.get('/deleted', response_model=List[UserOut], status_code=status.HTTP_200_OK)
def get_deleted_users(log_info: dict = Depends(log_sensitive_operation)):
    """Obtener usuarios eliminados - CON middleware de operación sensible"""
    try:
        return get_all_users_deleted()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener usuarios eliminados"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener usuarios eliminados"
        )

@users.get('/me', response_model=UserOut, status_code=status.HTTP_200_OK)
def get_current_user_profile(current_user: dict = Depends(get_current_user_token)):
    """Obtener perfil del usuario actual"""
    try:
        user_id = current_user["user_id"]
        user = get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
            
        return user
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener el perfil"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener el perfil"
        )

@users.get('/{user_id}', response_model=UserOut, status_code=status.HTTP_200_OK)
def get_user(user_id: str, log_info: dict = Depends(log_read_operation)):
    """Obtener un usuario por ID - CON middleware de lectura"""
    try:
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario es requerido"
            )
        
        user = get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        return user
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener el usuario"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener el usuario"
        )

@users.post('', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: UserCreate):
    """Crear un nuevo usuario - SIN middleware (registro público)"""
    try:
        return create_user(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El email ya está registrado"
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al crear el usuario"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al crear el usuario"
        )

@users.post('/insert', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def insert_user_endpoint(user: UserInsert, log_info: dict = Depends(log_sensitive_operation)):
    """Insertar usuario con datos predefinidos - CON middleware de operación sensible (para seeders)"""
    try:
        return insert_user(user)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error de datos duplicados"
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al insertar el usuario"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al insertar el usuario"
        )

@users.put('/{user_id}', response_model=UserOut, status_code=status.HTTP_200_OK)
def update_user_endpoint(user_id: str, user: UserUpdate, log_info: dict = Depends(log_sensitive_operation)):
    """Actualizar un usuario - CON middleware de operación sensible"""
    try:
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario es requerido"
            )
        return update_user(user_id, user)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email ya está registrado"
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al actualizar el usuario"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al actualizar el usuario"
        )

@users.delete('/{user_id}', status_code=status.HTTP_200_OK)
def delete_user_endpoint(user_id: str, log_info: dict = Depends(log_sensitive_operation)):
    """Eliminar un usuario (soft delete) - CON middleware de operación sensible"""
    try:
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario es requerido"
            )
        success = soft_delete_user(user_id)
        if success:
            return {"detail": f"Usuario {user_id} eliminado exitosamente"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar el usuario"
            )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al eliminar el usuario"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al eliminar el usuario"
        )

@users.post('/{user_id}/restore', response_model=UserOut, status_code=status.HTTP_200_OK)
def restore_user_endpoint(user_id: str, log_info: dict = Depends(log_sensitive_operation)):
    """Restaurar un usuario eliminado - CON middleware de operación sensible"""
    try:
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario es requerido"
            )
        return restore_user(user_id)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al restaurar el usuario"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al restaurar el usuario"
        )

@users.post('/login', response_model=Token, status_code=status.HTTP_200_OK)
def login_endpoint(login_data: UserLogin):
    """Login de usuario - SIN middleware (acceso público)"""
    try:
        return login_user(login_data.emails, login_data.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al iniciar sesión"
        )

@users.post('/{user_id}/roles', response_model=UserOut, status_code=status.HTTP_200_OK)
def assign_role_to_user(
    user_id: str,
    role_assignment: RoleAssignment,
    log_info: dict = Depends(log_sensitive_operation)
):
    """Asignar rol a un usuario - CON middleware de operación sensible"""
    try:
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario es requerido"
            )
        return assign_role(user_id, role_assignment.role_name)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al asignar el rol"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al asignar el rol"
        )

@users.delete('/{user_id}/roles/{role_name}', response_model=UserOut, status_code=status.HTTP_200_OK)
def remove_role_from_user(
    user_id: str,
    role_name: str,
    log_info: dict = Depends(log_sensitive_operation)
):
    """Remover rol de un usuario - CON middleware de operación sensible"""
    try:
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario es requerido"
            )
        
        if not role_name or not role_name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nombre de rol es requerido"
            )
        return remove_role(user_id, role_name)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al remover el rol"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al remover el rol"
        )