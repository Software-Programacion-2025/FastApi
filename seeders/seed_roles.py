"""
Seeder para la carga inicial de roles del sistema
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlite3 import IntegrityError
from config.cnx import SessionLocal, engine
from config.basemodel import Base
from roles.model import Rol
from config.associations import rol_permiso_association
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_roles_table():
    """Crear las tablas de roles si no existen"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas de roles creadas/verificadas exitosamente")
    except Exception as e:
        logger.error(f"❌ Error al crear tablas: {e}")
        raise

def seed_roles():
    """Cargar roles básicos en la base de datos"""
    db = SessionLocal()
    
    print("=== Iniciando carga de roles ===")
    
    # Definir roles del sistema con nombres consistentes para el sistema de permisos
    roles_data = [
        {
            "rol_nombre": "Administrador", 
            "rol_permisos": "all"
        },
        {
            "rol_nombre": "Gerente", 
            "rol_permisos": "manage"
        },
        {
            "rol_nombre": "Empleado", 
            "rol_permisos": "read,create"
        },
        {
            "rol_nombre": "Cajero", 
            "rol_permisos": "read,create,update"
        },
        {
            "rol_nombre": "Cliente", 
            "rol_permisos": "read,self"
        }
    ]
    
    try:
        roles_creados = 0
        
        for rol_info in roles_data:
            # Verificar si el rol ya existe
            existing_rol = db.query(Rol).filter(Rol.rol_nombre == rol_info["rol_nombre"]).first()
            
            if not existing_rol:
                nuevo_rol = Rol(
                    rol_nombre=rol_info["rol_nombre"],
                    rol_permisos=rol_info["rol_permisos"]
                )
                db.add(nuevo_rol)
                roles_creados += 1
                print(f"✓ Creando rol: {rol_info['rol_nombre']}")
                logger.info(f"📝 Creando rol: {rol_info['rol_nombre']}")
            else:
                print(f"- Rol '{rol_info['rol_nombre']}' ya existe, omitiendo...")
                logger.info(f"⚠️  Rol '{rol_info['rol_nombre']}' ya existe, omitiendo...")
        
        db.commit()
        
        if roles_creados > 0:
            print(f"✓ Se crearon {roles_creados} roles exitosamente")
            logger.info(f"✅ Se crearon {roles_creados} roles exitosamente")
        else:
            print("ℹ️ Todos los roles ya existían")
            logger.info("ℹ️  Todos los roles ya existían")
            
    except IntegrityError as e:
        db.rollback()
        print(f"✗ Error de integridad al crear roles: {e}")
        logger.error(f"❌ Error de integridad al crear roles: {e}")
        raise
    except Exception as e:
        db.rollback()
        print(f"✗ Error inesperado al crear roles: {e}")
        logger.error(f"❌ Error inesperado al crear roles: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Seeder de Roles ===")
    create_roles_table()
    seed_roles()
    print("=== Finalizado ===")