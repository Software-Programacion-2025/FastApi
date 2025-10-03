"""
Configuración centralizada de tablas para evitar problemas de orden de importación
"""
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from config.basemodel import Base
from sqlalchemy.dialects.sqlite import INTEGER

# Definir la tabla intermedia aquí para evitar problemas de importación circular
rol_permiso_association = Table(
    'rol_permiso', 
    Base.metadata,
    Column('rol_id', Integer, ForeignKey('roles.rol_id'), primary_key=True),
    Column('permiso_id', Integer, ForeignKey('permisos.permiso_id'), primary_key=True), 
    Column('created_at', DateTime, default=datetime.utcnow, nullable=False)
)

# Asociación entre usuarios y tareas
user_task_association = Table(
    'user_task_association',
    Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id'), primary_key=True),
    Column('task_id', INTEGER, ForeignKey('tasks.id'), primary_key=True)
)

# Asociación entre usuarios y roles (many-to-many)
user_rol_association = Table(
    'user_rol_association',
    Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id'), primary_key=True),
    Column('rol_id', Integer, ForeignKey('roles.rol_id'), primary_key=True),
    Column('assigned_at', DateTime, default=datetime.utcnow, nullable=False)
)