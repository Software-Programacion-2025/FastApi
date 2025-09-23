"""
Seeder para la carga inicial de permisos del sistema
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from sqlalchemy.exc import IntegrityError
from config.cnx import SessionLocal, engine
from config.basemodel import Base
from permisos.model import Permiso

def create_permissions_table():
    """Crear las tablas de permisos si no existen"""
    try:
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        print("✓ Tablas de permisos creadas correctamente")
    except Exception as e:
        print(f"✗ Error al crear tablas: {e}")

def seed_permisos():
    """Crear permisos básicos del sistema"""
    db = SessionLocal()
    
    try:
        print("=== Iniciando carga de permisos ===")
        
        # Definir permisos basados en las rutas reales existentes
        permisos_base = [
            # === PERMISOS DE USUARIOS ===
            {
                "permiso_nombre": "users.listar",
                "permiso_ruta": "/users",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Listar usuarios del sistema"
            },
            {
                "permiso_nombre": "users.listar_eliminados",
                "permiso_ruta": "/users/deleted",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Listar usuarios eliminados"
            },
            {
                "permiso_nombre": "users.crear",
                "permiso_ruta": "/users",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Crear nuevos usuarios"
            },
            {
                "permiso_nombre": "users.insertar",
                "permiso_ruta": "/users/insert",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Insertar usuario con validaciones adicionales"
            },
            {
                "permiso_nombre": "users.ver_perfil",
                "permiso_ruta": "/users/me",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Ver perfil del usuario autenticado"
            },
            {
                "permiso_nombre": "users.ver",
                "permiso_ruta": "/users/{id}",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Ver detalles de un usuario"
            },
            {
                "permiso_nombre": "users.actualizar",
                "permiso_ruta": "/users/{id}",
                "permiso_metodo": "PATCH",
                "permiso_descripcion": "Actualizar usuario"
            },
            {
                "permiso_nombre": "users.eliminar",
                "permiso_ruta": "/users/{id}",
                "permiso_metodo": "DELETE",
                "permiso_descripcion": "Eliminar usuario (soft delete)"
            },
            {
                "permiso_nombre": "users.restaurar",
                "permiso_ruta": "/users/{id}/restore",
                "permiso_metodo": "PATCH",
                "permiso_descripcion": "Restaurar usuario eliminado"
            },
            {
                "permiso_nombre": "users.login",
                "permiso_ruta": "/users/login",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Iniciar sesión"
            },
            
            # === PERMISOS DE TAREAS ===
            {
                "permiso_nombre": "tasks.listar",
                "permiso_ruta": "/tasks",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Listar todas las tareas"
            },
            {
                "permiso_nombre": "tasks.ver",
                "permiso_ruta": "/tasks/{id}",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Ver detalles de una tarea"
            },
            {
                "permiso_nombre": "tasks.crear",
                "permiso_ruta": "/tasks",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Crear nueva tarea"
            },
            {
                "permiso_nombre": "tasks.actualizar_estado",
                "permiso_ruta": "/tasks/{id}/state",
                "permiso_metodo": "PATCH",
                "permiso_descripcion": "Actualizar estado de una tarea"
            },
            {
                "permiso_nombre": "tasks.asignar_usuario",
                "permiso_ruta": "/tasks/{id}/assign",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Asignar usuario a una tarea"
            },
            {
                "permiso_nombre": "tasks.desasignar_usuario",
                "permiso_ruta": "/tasks/{id}/unassign",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Desasignar usuario de una tarea"
            },
            
            # === PERMISOS DE ROLES ===
            {
                "permiso_nombre": "roles.listar",
                "permiso_ruta": "/roles",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Listar roles del sistema"
            },
            {
                "permiso_nombre": "roles.crear",
                "permiso_ruta": "/roles",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Crear nuevos roles"
            },
            {
                "permiso_nombre": "roles.ver",
                "permiso_ruta": "/roles/{id}",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Ver detalles de un rol"
            },
            {
                "permiso_nombre": "roles.actualizar",
                "permiso_ruta": "/roles/{id}",
                "permiso_metodo": "PATCH",
                "permiso_descripcion": "Actualizar rol"
            },
            {
                "permiso_nombre": "roles.eliminar",
                "permiso_ruta": "/roles/{id}",
                "permiso_metodo": "DELETE",
                "permiso_descripcion": "Eliminar rol"
            },

            
            # === PERMISOS DE SISTEMA (DEFAULT) ===
            {
                "permiso_nombre": "system.home",
                "permiso_ruta": "/",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Acceso a la página de inicio"
            },
            {
                "permiso_nombre": "system.health",
                "permiso_ruta": "/health",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Verificar estado del sistema"
            },
            {
                "permiso_nombre": "system.docs",
                "permiso_ruta": "/docs",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Acceder a documentación de la API"
            },
            
            # === PERMISOS DE PERMISOS (META-PERMISOS) ===
            {
                "permiso_nombre": "permisos.listar",
                "permiso_ruta": "/permisos",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Listar permisos del sistema"
            },
            {
                "permiso_nombre": "permisos.crear",
                "permiso_ruta": "/permisos",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Crear nuevos permisos"
            },
            {
                "permiso_nombre": "permisos.ver",
                "permiso_ruta": "/permisos/{id}",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Ver detalles de un permiso"
            },
            {
                "permiso_nombre": "permisos.actualizar",
                "permiso_ruta": "/permisos/{id}",
                "permiso_metodo": "PATCH",
                "permiso_descripcion": "Actualizar permisos"
            },
            {
                "permiso_nombre": "permisos.eliminar",
                "permiso_ruta": "/permisos/{id}",
                "permiso_metodo": "DELETE",
                "permiso_descripcion": "Eliminar permisos"
            },
            {
                "permiso_nombre": "permisos.asignar_rol",
                "permiso_ruta": "/permisos/assign",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Asignar permisos a roles"
            },
            {
                "permiso_nombre": "permisos.remover_rol",
                "permiso_ruta": "/permisos/remove",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Remover permisos de roles"
            }
        ]
        
        permisos_creados = 0
        
        for permiso_data in permisos_base:
            # Verificar si el permiso ya existe
            existing = db.query(Permiso).filter(
                Permiso.permiso_ruta == permiso_data["permiso_ruta"],
                Permiso.permiso_metodo == permiso_data["permiso_metodo"]
            ).first()
            
            if not existing:
                permiso = Permiso(**permiso_data)
                db.add(permiso)
                permisos_creados += 1
                print(f"✓ Creado permiso: {permiso_data['permiso_nombre']}")
            else:
                print(f"- Ya existe permiso: {permiso_data['permiso_nombre']}")
        
        db.commit()
        print(f"\n✓ {permisos_creados} permisos creados correctamente")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error al crear permisos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Seeder de Permisos ===")
    create_permissions_table()
    seed_permisos()
    print("=== Finalizado ===")