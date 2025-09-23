"""
Seeder para la asignación de permisos a roles
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from sqlalchemy import text
from config.cnx import SessionLocal
from permisos.model import Permiso
from roles.model import Rol

def seed_rol_permisos():
    """Asignar permisos a roles existentes"""
    db = SessionLocal()
    
    try:
        print("=== Iniciando asignación de permisos a roles ===")
        
        # Obtener roles existentes
        roles = db.query(Rol).all()
        
        if not roles:
            print("⚠ No hay roles en el sistema. Ejecute primero el seeder de roles.")
            return
        
        # Obtener todos los permisos
        permisos = db.query(Permiso).all()
        permisos_dict = {}
        for p in permisos:
            permisos_dict[p.permiso_nombre] = p.permiso_id
        
        # Definir asignaciones de permisos por rol - ACTUALIZADAS según rutas reales
        rol_permisos_config = {
            "administrador": [
                # === PERMISOS COMPLETOS DE ADMINISTRADOR ===
                # Sistema
                "system.home", "system.health", "system.docs",
                # Usuarios
                "users.listar", "users.listar_eliminados", "users.crear", "users.insertar", 
                "users.ver_perfil", "users.ver", "users.actualizar", "users.eliminar", 
                "users.restaurar", "users.login",
                # Tareas
                "tasks.listar", "tasks.ver", "tasks.crear", "tasks.actualizar_estado",
                "tasks.asignar_usuario", "tasks.desasignar_usuario",
                # Roles
                "roles.listar", "roles.crear", "roles.ver", "roles.actualizar", "roles.eliminar",
                # Permisos (meta-administración)
                "permisos.listar", "permisos.crear", "permisos.ver", "permisos.actualizar", 
                "permisos.eliminar", "permisos.asignar_rol", "permisos.remover_rol"
            ],
            "gerente": [
                # === PERMISOS DE GESTIÓN PARA GERENTE ===
                # Sistema
                "system.home", "system.health",
                # Usuarios (lectura y actualización limitada)
                "users.listar", "users.ver_perfil", "users.ver", "users.actualizar", "users.login",
                # Tareas (gestión completa)
                "tasks.listar", "tasks.ver", "tasks.crear", "tasks.actualizar_estado",
                "tasks.asignar_usuario", "tasks.desasignar_usuario",
                # Roles (solo lectura)
                "roles.listar", "roles.ver",
                # Permisos (solo lectura)
                "permisos.listar", "permisos.ver"
            ],
            "empleado": [
                # === PERMISOS BÁSICOS PARA EMPLEADO ===
                # Sistema
                "system.home",
                # Usuarios (solo perfil propio)
                "users.ver_perfil", "users.login",
                # Tareas (lectura y gestión limitada)
                "tasks.listar", "tasks.ver", "tasks.actualizar_estado"
            ],
            "cliente": [
                # === PERMISOS PARA CLIENTE ===
                # Sistema
                "system.home",
                # Usuarios (perfil propio)
                "users.ver_perfil", "users.actualizar", "users.login",
                # Tareas (solo ver las asignadas)
                "tasks.listar", "tasks.ver", "tasks.actualizar_estado"
            ]
        }
        
        asignaciones_realizadas = 0
        
        for rol in roles:
            rol_nombre = rol.rol_nombre.lower()
            
            if rol_nombre in rol_permisos_config:
                # Limpiar asignaciones existentes para este rol
                delete_sql = text("DELETE FROM rol_permiso WHERE rol_id = :rol_id")
                db.execute(delete_sql, {"rol_id": rol.rol_id})
                
                # Asignar nuevos permisos
                permisos_rol = rol_permisos_config[rol_nombre]
                
                permisos_asignados = 0
                for permiso_nombre in permisos_rol:
                    if permiso_nombre in permisos_dict:
                        permiso_id = permisos_dict[permiso_nombre]
                        insert_sql = text("""
                            INSERT INTO rol_permiso (rol_id, permiso_id, created_at) 
                            VALUES (:rol_id, :permiso_id, :created_at)
                        """)
                        db.execute(insert_sql, {
                            "rol_id": rol.rol_id,
                            "permiso_id": permiso_id,
                            "created_at": datetime.utcnow()
                        })
                        permisos_asignados += 1
                        asignaciones_realizadas += 1
                    else:
                        print(f"⚠ Permiso '{permiso_nombre}' no encontrado")
                
                print(f"✓ Asignados {permisos_asignados} permisos al rol '{rol.rol_nombre}'")
            else:
                print(f"⚠ No hay configuración de permisos para el rol '{rol.rol_nombre}'")
        
        db.commit()
        print(f"\n✓ {asignaciones_realizadas} asignaciones de permisos realizadas correctamente")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error al asignar permisos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Seeder de Asignación Rol-Permisos ===")
    seed_rol_permisos()
    print("=== Finalizado ===")