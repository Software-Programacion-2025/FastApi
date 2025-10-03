"""
Seeder para la carga inicial de tareas del sistema
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlite3 import IntegrityError
from config.cnx import SessionLocal, engine
from config.basemodel import Base
from tasks.model import Task
from users.model import User
from datetime import datetime
import logging

# Configurar logging para seeders
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('sqlalchemy').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.engine').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)

def create_tasks_table():
    """Crear las tablas de tareas si no existen"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas de tareas creadas/verificadas exitosamente")
    except Exception as e:
        logger.error(f"❌ Error al crear tablas: {e}")
        raise

def seed_tasks():
    """Cargar tareas básicas en la base de datos"""
    db = SessionLocal()
    
    print("=== Iniciando carga de tareas ===")
    
    try:
        # Obtener algunos usuarios para asignar a las tareas
        usuarios = db.query(User).all()
        
        if not usuarios:
            print("⚠ Debe existir al menos un usuario antes de crear tareas")
            logger.error("❌ Debe existir al menos un usuario antes de crear tareas")
            return
        
        # Tomar el primer usuario para asignar las tareas
        usuario_admin = usuarios[0]
        
        # Definir tareas del sistema
        tasks_data = [
            {
                "title": "Configurar sistema de autenticación",
                "description": "Implementar sistema de login con JWT y middleware de autenticación",
                "state": "completed"
            },
            {
                "title": "Crear modelo de usuarios",
                "description": "Diseñar y implementar el modelo User con todas sus relaciones",
                "state": "completed"
            },
            {
                "title": "Implementar CRUD de tareas",
                "description": "Crear endpoints para crear, leer, actualizar y eliminar tareas",
                "state": "in_progress"
            },
            {
                "title": "Sistema de asignación de usuarios",
                "description": "Permitir asignar y desasignar usuarios a tareas específicas",
                "state": "in_progress"
            },
            {
                "title": "Documentación de API",
                "description": "Completar la documentación Swagger de todos los endpoints",
                "state": "pending"
            },
            {
                "title": "Testing unitario",
                "description": "Escribir tests unitarios para todos los servicios y endpoints",
                "state": "pending"
            },
            {
                "title": "Optimización de consultas",
                "description": "Revisar y optimizar las consultas de base de datos para mejor rendimiento",
                "state": "pending"
            },
            {
                "title": "Sistema de notificaciones",
                "description": "Implementar notificaciones cuando se asignan o completan tareas",
                "state": "pending"
            }
        ]
        
        tasks_creadas = 0
        
        for task_info in tasks_data:
            # Verificar si la tarea ya existe
            existing_task = db.query(Task).filter(
                Task.title == task_info["title"]
            ).first()
            
            if not existing_task:
                nueva_task = Task(
                    title=task_info["title"],
                    description=task_info["description"],
                    state=task_info["state"],
                    create_at=datetime.now()
                )
                
                db.add(nueva_task)
                db.flush()  # Para obtener el ID
                
                # Asignar al usuario admin
                nueva_task.users.append(usuario_admin)
                
                tasks_creadas += 1
                print(f"✓ Creando tarea: {task_info['title']} - Estado: {task_info['state']}")
                logger.info(f"📋 Creando tarea: {task_info['title']} - Estado: {task_info['state']}")
            else:
                print(f"- Tarea '{task_info['title']}' ya existe, omitiendo...")
                logger.info(f"⚠️  Tarea '{task_info['title']}' ya existe, omitiendo...")
        
        db.commit()
        
        if tasks_creadas > 0:
            print(f"✓ Se crearon {tasks_creadas} tareas exitosamente")
            logger.info(f"✅ Se crearon {tasks_creadas} tareas exitosamente")
        else:
            print("ℹ️ Todas las tareas ya existían")
            logger.info("ℹ️  Todas las tareas ya existían")
            
    except IntegrityError as e:
        db.rollback()
        print(f"✗ Error de integridad al crear tareas: {e}")
        logger.error(f"❌ Error de integridad al crear tareas: {e}")
        raise
    except Exception as e:
        db.rollback()
        print(f"✗ Error inesperado al crear tareas: {e}")
        logger.error(f"❌ Error inesperado al crear tareas: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Seeder de Tareas ===")
    create_tasks_table()
    seed_tasks()
    print("=== Finalizado ===")