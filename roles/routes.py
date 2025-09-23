from fastapi import APIRouter, HTTPException, status
from typing import List
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .dto import RolCreate, RolOut, RolUpdate
from .services import get_all_roles, get_rol_by_id, create_rol, update_rol, delete_rol

roles = APIRouter()


@roles.get('', response_model=List[RolOut], status_code=status.HTTP_200_OK)
def get_roles():
    """Obtener todos los roles"""
    try:
        return get_all_roles()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener los roles"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener los roles"
        )


@roles.get('/{rol_id}', response_model=RolOut, status_code=status.HTTP_200_OK)
def get_rol(rol_id: int):
    """Obtener un rol por ID"""
    try:
        if rol_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de rol debe ser un número positivo"
            )

        rol = get_rol_by_id(rol_id)
        if not rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rol con ID {rol_id} no encontrado"
            )
        return rol
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener el rol"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener el rol"
        )


@roles.post('', response_model=RolOut, status_code=status.HTTP_201_CREATED)
def post_rol(rol: RolCreate):
    """Crear un nuevo rol"""
    try:
        if not rol.rol_nombre or rol.rol_nombre.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del rol es obligatorio"
            )

        return create_rol(rol)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error de integridad de datos al crear el rol"
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al crear el rol"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al crear el rol"
        )


@roles.patch('/{rol_id}', response_model=RolOut, status_code=status.HTTP_200_OK)
def patch_rol(rol_id: int, update_data: RolUpdate):
    """Actualizar campos de un rol existente"""
    try:
        if rol_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de rol debe ser un número positivo"
            )

        return update_rol(rol_id, update_data)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al actualizar el rol"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al actualizar el rol"
        )


@roles.delete('/{rol_id}', status_code=status.HTTP_200_OK)
def delete_rol_route(rol_id: int):
    """Eliminar un rol por ID"""
    try:
        if rol_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de rol debe ser un número positivo"
            )

        result = delete_rol(rol_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rol con ID {rol_id} no encontrado"
            )
        return {"detail": f"Rol con ID {rol_id} eliminado exitosamente"}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al eliminar el rol"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al eliminar el rol"
        )