"""
Seeder para la carga inicial de usuarios del sistema
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
from sqlite3 import IntegrityError
from config.cnx import SessionLocal, engine
from config.basemodel import Base
from users.model import User
from middlewares.auth import hash_password
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_users_table():
    """Crear las tablas de usuarios si no existen"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas de usuarios creadas/verificadas exitosamente")
    except Exception as e:
        logger.error(f"❌ Error al crear tablas: {e}")
        raise

def seed_usuarios():
    """Cargar usuarios básicos en la base de datos con contraseñas encriptadas usando bcrypt"""
    db = SessionLocal()
    
    print("=== Iniciando carga de usuarios ===")
    print("ℹ️ Las contraseñas se encriptarán usando bcrypt")
    
    try:
        
        # Definir usuarios del sistema con el nuevo formato User
        usuarios_data = [
            {
                "id": str(uuid.uuid4()),
                "firstName": "Admin",
                "lastName": "Sistema",
                "emails": "admin@sistema.com",
                "password": "admin123",
                "ages": 35
            },
            {
                "id": str(uuid.uuid4()),
                "firstName": "María",
                "lastName": "González",
                "emails": "maria.gonzalez@empresa.com", 
                "password": "gerente123",
                "ages": 42
            },
            {
                "id": str(uuid.uuid4()),
                "firstName": "Juan",
                "lastName": "Pérez",
                "emails": "juan.perez@empresa.com",
                "password": "empleado123",
                "ages": 28
            },
            {
                "id": str(uuid.uuid4()),
                "firstName": "Ana",
                "lastName": "López",
                "emails": "ana.lopez@empresa.com",
                "password": "cajero123",
                "ages": 25
            }
        ]
        
        usuarios_creados = 0
        
        for usuario_info in usuarios_data:
            # Verificar si el usuario ya existe
            existing_usuario = db.query(User).filter(
                User.emails == usuario_info["emails"]
            ).first()
            
            if not existing_usuario:
                # Encriptar la contraseña antes de guardarla
                hashed_password = hash_password(usuario_info["password"])
                
                nuevo_usuario = User(
                    id=usuario_info["id"],
                    firstName=usuario_info["firstName"],
                    lastName=usuario_info["lastName"],
                    emails=usuario_info["emails"],
                    password=hashed_password,
                    ages=usuario_info["ages"]
                )
                db.add(nuevo_usuario)
                usuarios_creados += 1
                print(f"✓ Creando usuario: {usuario_info['emails']} ({usuario_info['firstName']} {usuario_info['lastName']}) - Contraseña encriptada")
                logger.info(f"👤 Creando usuario: {usuario_info['emails']} ({usuario_info['firstName']} {usuario_info['lastName']})")
            else:
                print(f"- Usuario '{usuario_info['emails']}' ya existe, omitiendo...")
                logger.info(f"⚠️  Usuario '{usuario_info['emails']}' ya existe, omitiendo...")
        
        db.commit()
        
        if usuarios_creados > 0:
            print(f"✓ Se crearon {usuarios_creados} usuarios exitosamente")
            logger.info(f"✅ Se crearon {usuarios_creados} usuarios exitosamente")
        else:
            print("ℹ️ Todos los usuarios ya existían")
            logger.info("ℹ️  Todos los usuarios ya existían")
            
    except IntegrityError as e:
        db.rollback()
        print(f"✗ Error de integridad al crear usuarios: {e}")
        logger.error(f"❌ Error de integridad al crear usuarios: {e}")
        raise
    except Exception as e:
        db.rollback()
        print(f"✗ Error inesperado al crear usuarios: {e}")
        logger.error(f"❌ Error inesperado al crear usuarios: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Seeder de Usuarios ===")
    create_users_table()
    seed_usuarios()
    print("=== Finalizado ===")