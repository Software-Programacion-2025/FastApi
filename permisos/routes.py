from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from config.cnx import get_db
from permisos.services import PermisoService
from permisos.dto import (
    PermisoCreate, 
    PermisoUpdate, 
    PermisoResponse, 
    RolPermisoAssign, 
    RolPermisoRemove,
    PermisoWithRoles,
    RolWithPermisos
)
from middlewares.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[PermisoResponse])
async def get_permisos(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=100, description="Número máximo de registros a devolver"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtener lista de permisos con paginación"""
    service = PermisoService(db)
    permisos = service.get_all_permisos(skip=skip, limit=limit, activo=activo)
    return permisos

@router.get("/{permiso_id}", response_model=PermisoWithRoles)
async def get_permiso(
    permiso_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtener un permiso por ID con sus roles asociados"""
    service = PermisoService(db)
    permiso = service.get_permiso_by_id(permiso_id)
    if not permiso:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return permiso

@router.post("/", response_model=PermisoResponse, status_code=201)
async def create_permiso(
    permiso_data: PermisoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Crear un nuevo permiso"""
    service = PermisoService(db)
    return service.create_permiso(permiso_data)

@router.put("/{permiso_id}", response_model=PermisoResponse)
async def update_permiso(
    permiso_id: int,
    permiso_data: PermisoUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Actualizar un permiso"""
    service = PermisoService(db)
    permiso = service.update_permiso(permiso_id, permiso_data)
    if not permiso:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return permiso

@router.delete("/{permiso_id}")
async def delete_permiso(
    permiso_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Eliminar un permiso"""
    service = PermisoService(db)
    success = service.delete_permiso(permiso_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return {"message": "Permiso eliminado correctamente"}

@router.get("/ruta/{ruta}/metodo/{metodo}", response_model=PermisoResponse)
async def get_permiso_by_ruta_metodo(
    ruta: str,
    metodo: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtener permiso por ruta y método"""
    service = PermisoService(db)
    permiso = service.get_permiso_by_ruta_metodo(ruta, metodo)
    if not permiso:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return permiso

# Rutas para gestión de relaciones rol-permiso
@router.post("/rol/assign")
async def assign_permisos_to_rol(
    assign_data: RolPermisoAssign,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Asignar permisos a un rol (reemplaza los permisos existentes)"""
    service = PermisoService(db)
    result = service.assign_permisos_to_rol(assign_data)
    return result

@router.post("/rol/remove")
async def remove_permisos_from_rol(
    remove_data: RolPermisoRemove,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Remover permisos específicos de un rol"""
    service = PermisoService(db)
    result = service.remove_permisos_from_rol(remove_data)
    return result

@router.get("/rol/{rol_id}", response_model=RolWithPermisos)
async def get_rol_permisos(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtener rol con sus permisos asociados"""
    service = PermisoService(db)
    rol_permisos = service.get_rol_permisos(rol_id)
    if not rol_permisos:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol_permisos

@router.get("/usuario/{user_rol_id}/permisos", response_model=List[PermisoResponse])
async def get_user_permissions(
    user_rol_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtener todos los permisos de un usuario basado en su rol"""
    service = PermisoService(db)
    permisos = service.get_user_permissions(user_rol_id)
    return permisos

@router.post("/usuario/verify")
async def verify_user_permission(
    user_rol_id: int,
    ruta: str,
    metodo: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Verificar si un usuario tiene permiso para una ruta y método específico"""
    service = PermisoService(db)
    has_permission = service.user_has_permission(user_rol_id, ruta, metodo)
    return {
        "has_permission": has_permission,
        "user_rol_id": user_rol_id,
        "ruta": ruta,
        "metodo": metodo
    }