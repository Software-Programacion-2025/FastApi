from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from config.basemodel import Base
from config.associations import rol_permiso_association

class Permiso(Base):
    __tablename__ = "permisos"
    
    permiso_id = Column(Integer, primary_key=True, autoincrement=True)
    permiso_nombre = Column(String(100), nullable=False, unique=True)
    permiso_ruta = Column(String(255), nullable=False)
    permiso_metodo = Column(String(10), nullable=False)  # GET, POST, PUT, DELETE, PATCH
    permiso_descripcion = Column(String(500))
    permiso_activo = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relación many-to-many con roles
    roles = relationship("Rol", secondary=rol_permiso_association, back_populates="permisos")
    
    def __repr__(self):
        return f"<Permiso(id={self.permiso_id}, nombre='{self.permiso_nombre}', ruta='{self.permiso_ruta}', metodo='{self.permiso_metodo}')>"