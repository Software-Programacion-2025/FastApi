from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from datetime import datetime
import re

class PermisoBase(BaseModel):
    permiso_nombre: str = Field(..., min_length=1, max_length=100, description="Nombre único del permiso")
    permiso_ruta: str = Field(..., min_length=1, max_length=255, description="Ruta del endpoint")
    permiso_metodo: Literal["GET", "POST", "PUT", "DELETE", "PATCH"] = Field(..., description="Método HTTP")
    permiso_descripcion: Optional[str] = Field(None, max_length=500, description="Descripción del permiso")
    permiso_activo: bool = Field(True, description="Estado del permiso")

class PermisoCreate(PermisoBase):
    pass

class PermisoUpdate(BaseModel):
    permiso_nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    permiso_ruta: Optional[str] = Field(None, min_length=1, max_length=255)
    permiso_metodo: Optional[Literal["GET", "POST", "PUT", "DELETE", "PATCH"]] = None
    permiso_descripcion: Optional[str] = Field(None, max_length=500)
    permiso_activo: Optional[bool] = None

class PermisoResponse(PermisoBase):
    permiso_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RolPermisoAssign(BaseModel):
    rol_id: int = Field(..., description="ID del rol")
    permiso_ids: List[int] = Field(..., description="Lista de IDs de permisos a asignar")

class RolPermisoRemove(BaseModel):
    rol_id: int = Field(..., description="ID del rol")
    permiso_ids: List[int] = Field(..., description="Lista de IDs de permisos a remover")

class PermisoWithRoles(PermisoResponse):
    roles: List[dict] = Field(default=[], description="Lista de roles que tienen este permiso")

class RolWithPermisos(BaseModel):
    rol_id: int
    rol_nombre: str
    permisos: List[PermisoResponse] = Field(default=[], description="Lista de permisos del rol")

    class Config:
        from_attributes = True