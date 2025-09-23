from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException
from permisos.model import Permiso
from permisos.dto import PermisoCreate, PermisoUpdate, RolPermisoAssign, RolPermisoRemove
from roles.model import Rol

class PermisoService:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_permisos(self, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[Permiso]:
        """Obtener todos los permisos con paginación"""
        query = self.db.query(Permiso)
        
        if activo is not None:
            query = query.filter(Permiso.permiso_activo == activo)
            
        return query.offset(skip).limit(limit).all()
    
    def get_permiso_by_id(self, permiso_id: int) -> Optional[Permiso]:
        """Obtener permiso por ID"""
        return self.db.query(Permiso).filter(
            Permiso.permiso_id == permiso_id
        ).first()
    
    def get_permiso_by_ruta_metodo(self, ruta: str, metodo: str) -> Optional[Permiso]:
        """Obtener permiso por ruta y método"""
        return self.db.query(Permiso).filter(
            Permiso.permiso_ruta == ruta,
            Permiso.permiso_metodo == metodo,
            Permiso.permiso_activo == True
        ).first()
    
    def create_permiso(self, permiso_data: PermisoCreate) -> Permiso:
        """Crear un nuevo permiso"""
        try:
            # Verificar si ya existe un permiso con la misma ruta y método
            existing = self.get_permiso_by_ruta_metodo(
                permiso_data.permiso_ruta, 
                permiso_data.permiso_metodo
            )
            if existing:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Ya existe un permiso para la ruta {permiso_data.permiso_ruta} con método {permiso_data.permiso_metodo}"
                )
            
            permiso = Permiso(**permiso_data.model_dump())
            self.db.add(permiso)
            self.db.commit()
            self.db.refresh(permiso)
            return permiso
        except IntegrityError as e:
            self.db.rollback()
            if "permiso_nombre" in str(e):
                raise HTTPException(status_code=400, detail="Ya existe un permiso con ese nombre")
            raise HTTPException(status_code=400, detail="Error al crear el permiso")
    
    def update_permiso(self, permiso_id: int, permiso_data: PermisoUpdate) -> Optional[Permiso]:
        """Actualizar un permiso"""
        permiso = self.get_permiso_by_id(permiso_id)
        if not permiso:
            return None
        
        try:
            # Si se está actualizando ruta o método, verificar que no exista la combinación
            if permiso_data.permiso_ruta or permiso_data.permiso_metodo:
                new_ruta = permiso_data.permiso_ruta if permiso_data.permiso_ruta else permiso.permiso_ruta
                new_metodo = permiso_data.permiso_metodo if permiso_data.permiso_metodo else permiso.permiso_metodo
                
                existing = self.get_permiso_by_ruta_metodo(new_ruta, new_metodo) # type: ignore
                if existing and existing.permiso_id != permiso_id: # type: ignore
                    raise HTTPException(
                        status_code=400,
                        detail=f"Ya existe un permiso para la ruta {new_ruta} con método {new_metodo}"
                    )
            
            # Actualizar campos
            for field, value in permiso_data.model_dump(exclude_unset=True).items():
                setattr(permiso, field, value)
            
            self.db.commit()
            self.db.refresh(permiso)
            return permiso
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Error al actualizar el permiso")
    
    def delete_permiso(self, permiso_id: int) -> bool:
        """Eliminar un permiso"""
        permiso = self.get_permiso_by_id(permiso_id)
        if not permiso:
            return False
        
        try:
            self.db.delete(permiso)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="No se puede eliminar el permiso porque está en uso")
    
    def assign_permisos_to_rol(self, assign_data: RolPermisoAssign) -> dict:
        """Asignar permisos a un rol"""
        rol = self.db.query(Rol).filter(Rol.rol_id == assign_data.rol_id).first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        
        # Verificar que todos los permisos existen
        permisos = self.db.query(Permiso).filter(
            Permiso.permiso_id.in_(assign_data.permiso_ids),
            Permiso.permiso_activo == True
        ).all()
        
        if len(permisos) != len(assign_data.permiso_ids):
            raise HTTPException(status_code=404, detail="Algunos permisos no fueron encontrados")
        
        try:
            # Eliminar asignaciones existentes
            delete_sql = text("DELETE FROM rol_permisos WHERE rol_id = :rol_id")
            self.db.execute(delete_sql, {"rol_id": assign_data.rol_id})
            
            # Insertar nuevas asignaciones
            for permiso_id in assign_data.permiso_ids:
                insert_sql = text("""
                    INSERT INTO rol_permisos (rol_id, permiso_id, created_at) 
                    VALUES (:rol_id, :permiso_id, :created_at)
                """)
                self.db.execute(insert_sql, {
                    "rol_id": assign_data.rol_id,
                    "permiso_id": permiso_id,
                    "created_at": datetime.utcnow()
                })
            
            self.db.commit()
            return {"message": "Permisos asignados correctamente", "rol_id": assign_data.rol_id}
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Error al asignar permisos")
    
    def remove_permisos_from_rol(self, remove_data: RolPermisoRemove) -> dict:
        """Remover permisos específicos de un rol"""
        rol = self.db.query(Rol).filter(Rol.rol_id == remove_data.rol_id).first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        
        try:
            # Remover permisos específicos
            for permiso_id in remove_data.permiso_ids:
                delete_sql = text("""
                    DELETE FROM rol_permisos 
                    WHERE rol_id = :rol_id AND permiso_id = :permiso_id
                """)
                self.db.execute(delete_sql, {
                    "rol_id": remove_data.rol_id,
                    "permiso_id": permiso_id
                })
            
            self.db.commit()
            return {"message": "Permisos removidos correctamente", "rol_id": remove_data.rol_id}
        except Exception:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Error al remover permisos")
    
    def get_rol_permisos(self, rol_id: int) -> Optional[dict]:
        """Obtener rol con sus permisos"""
        rol = self.db.query(Rol).filter(Rol.rol_id == rol_id).first()
        if not rol:
            return None
            
        # Usar SQL directo para evitar problemas con joins
        permisos_sql = text("""
            SELECT p.* FROM permisos p 
            INNER JOIN rol_permisos rp ON p.permiso_id = rp.permiso_id 
            WHERE rp.rol_id = :rol_id AND p.permiso_activo = 1
        """)
        result = self.db.execute(permisos_sql, {"rol_id": rol_id})
        
        permisos = []
        for row in result:
            permiso = self.db.query(Permiso).filter(Permiso.permiso_id == row.permiso_id).first()
            if permiso:
                permisos.append(permiso)
        
        return {
            "rol_id": rol.rol_id,
            "rol_nombre": rol.rol_nombre,
            "permisos": permisos
        }
    
    def user_has_permission(self, user_rol_id: int, ruta: str, metodo: str) -> bool:
        """Verificar si un usuario tiene permiso para una ruta y método específico"""
        # Verificar si existe el permiso usando SQL directo
        permission_sql = text("""
            SELECT COUNT(*) as count FROM permisos p 
            INNER JOIN rol_permiso rp ON p.permiso_id = rp.permiso_id 
            WHERE rp.rol_id = :rol_id 
            AND p.permiso_ruta = :ruta 
            AND p.permiso_metodo = :metodo 
            AND p.permiso_activo = 1
        """)
        result = self.db.execute(permission_sql, {
            "rol_id": user_rol_id,
            "ruta": ruta,
            "metodo": metodo
        })
        
        count = result.fetchone()
        return count[0] > 0 if count else False
    
    def get_user_permissions(self, user_rol_id: int) -> List[Permiso]:
        """Obtener todos los permisos de un usuario basado en su rol"""
        # Obtener permisos usando SQL directo
        permisos_sql = text("""
            SELECT p.* FROM permisos p 
            INNER JOIN rol_permiso rp ON p.permiso_id = rp.permiso_id 
            WHERE rp.rol_id = :rol_id AND p.permiso_activo = 1
        """)
        result = self.db.execute(permisos_sql, {"rol_id": user_rol_id})
        
        permisos = []
        for row in result:
            permiso = self.db.query(Permiso).filter(Permiso.permiso_id == row.permiso_id).first()
            if permiso:
                permisos.append(permiso)
        
        return permisos