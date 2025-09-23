from pydantic import BaseModel
from typing import Optional


class RolBase(BaseModel):
    rol_nombre: str
    rol_permisos: Optional[str] = None


class RolCreate(RolBase):
    """DTO para crear un rol"""
    class Config:
        json_schema_extra = {
            "example": {
                "rol_nombre": "Administrador",
                "rol_permisos": "crear,editar,eliminar,ver"
            }
        }


class RolUpdate(BaseModel):
    """DTO para actualizar un rol"""
    rol_nombre: Optional[str] = None
    rol_permisos: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "rol_nombre": "Editor",
                "rol_permisos": "editar,ver"
            }
        }


class RolOut(RolBase):
    """DTO para devolver un rol"""
    rol_id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "rol_id": 1,
                "rol_nombre": "Administrador",
                "rol_permisos": "crear,editar,eliminar,ver"
            }
        }