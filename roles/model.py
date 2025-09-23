from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from config.basemodel import Base
from config.associations import rol_permiso_association

class Rol(Base):
    __tablename__ = "roles"
    rol_id = Column (Integer, primary_key=True, autoincrement=True)
    rol_nombre = Column (String (50), nullable=False, unique=True)
    rol_permisos = Column (String (200))  # Ampliado y mantenido por compatibilidad
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relación many-to-many con permisos
    permisos = relationship("Permiso", secondary=rol_permiso_association, back_populates="roles")