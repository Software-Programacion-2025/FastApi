from fastapi import APIRouter, HTTPException, status
from uuid import uuid4
from typing import List
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import re
from .dto import *
from .services import getAllUsers, getAllUsersDeleted, getOneUser, postUser, putUser, deleteUser, recoveryUser

users = APIRouter()

def validate_email(email: str) -> bool:
    """Validar formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_uuid(uuid_string: str) -> bool:
    """Validar formato de UUID"""
    try:
        uuid_obj = uuid4()
        # Intentar crear un UUID desde el string
        from uuid import UUID
        UUID(uuid_string)
        return True
    except ValueError:
        return False

@users.get('', response_model=List[UserOut], status_code=status.HTTP_200_OK)
def get_all_users():
    """Obtener todos los usuarios activos"""
    try:
        return getAllUsers()
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

@users.get('/usersdeleted', response_model=List[UserOut], status_code=status.HTTP_200_OK)
def get_all_users_deleted():
    """Obtener todos los usuarios eliminados"""
    try:
        return getAllUsersDeleted()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener los usuarios eliminados"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener los usuarios eliminados"
        )

@users.get('/{id}', response_model=UserOut, status_code=status.HTTP_200_OK)
def get_one_user(id: str):
    """Obtener un usuario por ID"""
    try:
        if not id or not id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario es requerido"
            )
        
        if not validate_uuid(id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de ID de usuario inválido"
            )
        
        user = getOneUser(id=id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {id} no encontrado"
            )
        return user
    except HTTPException:
        raise
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
def post_user(user: UserInsert):
    """Crear un nuevo usuario"""
    try:
        # Validaciones de entrada
        if not user.firstName or not user.firstName.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre es requerido"
            )
        
        if not user.lastName or not user.lastName.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El apellido es requerido"
            )
        
        if not user.emails or not user.emails.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email es requerido"
            )
        
        if not validate_email(user.emails):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de email inválido"
            )
        
        if user.ages <= 0 or user.ages > 150:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La edad debe estar entre 1 y 150 años"
            )
        
        if not user.password or len(user.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña debe tener al menos 6 caracteres"
            )
        
        item = postUser(user)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se pudo crear el usuario. Es posible que el email ya exista"
            )
        return item
    except HTTPException:
        raise
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email ya está registrado"
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

@users.put('/{id}', response_model=UserOut, status_code=status.HTTP_200_OK)
def put_user(id: str, user: UserUpdate):
    """Actualizar un usuario existente"""
    try:
        if not id or not id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario es requerido"
            )
        
        if not validate_uuid(id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de ID de usuario inválido"
            )
        
        # Validaciones de entrada
        if not user.firstName or not user.firstName.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre es requerido"
            )
        
        if not user.lastName or not user.lastName.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El apellido es requerido"
            )
        
        if not user.emails or not user.emails.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email es requerido"
            )
        
        if not validate_email(user.emails):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de email inválido"
            )
        
        if user.ages <= 0 or user.ages > 150:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La edad debe estar entre 1 y 150 años"
            )
        
        item = putUser(id=id, user=user)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {id} no encontrado"
            )
        return item
    except HTTPException:
        raise
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email ya está registrado por otro usuario"
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

@users.delete('/recovery/{id}', status_code=status.HTTP_200_OK)
def delete_user_recovery(id: str):
    """Recuperar un usuario eliminado"""
    try:
        if not id or not id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario es requerido"
            )
        
        if not validate_uuid(id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de ID de usuario inválido"
            )
        
        if recoveryUser(id=id):
            return {"message": "Usuario recuperado exitosamente"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado o no se pudo recuperar"
            )
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al recuperar el usuario"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al recuperar el usuario"
        )

@users.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_user(id: str):
    """Eliminar un usuario (soft delete)"""
    try:
        if not id or not id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario es requerido"
            )
        
        if not validate_uuid(id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de ID de usuario inválido"
            )
        
        if deleteUser(id=id):
            return {"message": "Usuario eliminado exitosamente"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado o ya está eliminado"
            )
    except HTTPException:
        raise
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


