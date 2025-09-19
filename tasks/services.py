from .model import Task, user_task_association
from users.model import User
from config.cnx import SessionLocal
from .dto import TaskCreate, TaskUpdateState, TaskAssignUser
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_all_tasks():
    """Obtener todas las tareas con sus usuarios asignados"""
    db = None
    try:
        db = SessionLocal()
        tasks = db.query(Task).options(joinedload(Task.users)).all()
        logger.info(f"Se obtuvieron {len(tasks)} tareas exitosamente")
        return tasks
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener tareas: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al obtener tareas: {str(e)}")
        raise Exception("Error interno al obtener las tareas")
    finally:
        if db:
            db.close()

def create_task(task_data: TaskCreate):
    """Crear una nueva tarea y asignar el usuario creador"""
    db = None
    try:
        db = SessionLocal()
        
        # Verificar que el usuario existe y está activo
        user = db.query(User).filter(User.id == task_data.user_id, User.delete_at == None).first()
        if not user:
            logger.warning(f"Intento de crear tarea con usuario inexistente: {task_data.user_id}")
            raise ValueError("Usuario no encontrado o inactivo")
        
        # Crear la tarea
        task = Task(
            title=task_data.title.strip(),
            description=task_data.description.strip() if task_data.description else None,
            state=task_data.state
        )
        
        db.add(task)
        db.flush()  # Para obtener el ID sin confirmar la transacción
        
        # Asociar el usuario creador con la tarea
        task.users.append(user)
        db.commit()
        db.refresh(task)
        
        logger.info(f"Tarea creada exitosamente: ID {task.id}, Título: {task.title}")
        return task
        
    except ValueError:
        if db:
            db.rollback()
        raise
    except IntegrityError as e:
        if db:
            db.rollback()
        logger.error(f"Error de integridad al crear tarea: {str(e)}")
        raise IntegrityError("Error de integridad de datos", None, e)
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al crear tarea: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al crear tarea: {str(e)}")
        raise Exception("Error interno al crear la tarea")
    finally:
        if db:
            db.close()

def update_task_state(task_id: int, state_data: TaskUpdateState):
    """Actualizar el estado de una tarea"""
    db = None
    try:
        db = SessionLocal()
        
        # Validar que el task_id sea válido
        if task_id <= 0:
            raise ValueError("ID de tarea inválido")
        
        task = db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            logger.warning(f"Intento de actualizar tarea inexistente: {task_id}")
            raise ValueError("Tarea no encontrada")
        
        old_state = getattr(task, 'state', 'unknown')
        setattr(task, 'state', state_data.state.strip())
        
        db.commit()
        
        # Recargar la tarea con eager loading para evitar problemas de sesión
        updated_task = db.query(Task).options(joinedload(Task.users)).filter(Task.id == task_id).first()
        
        logger.info(f"Estado de tarea {task_id} actualizado de '{old_state}' a '{getattr(updated_task, 'state', 'unknown')}'")
        return updated_task
        
    except ValueError:
        if db:
            db.rollback()
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al actualizar tarea: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al actualizar tarea: {str(e)}")
        raise Exception("Error interno al actualizar la tarea")
    finally:
        if db:
            db.close()

def get_task_by_id(task_id: int):
    """Obtener una tarea por su ID con usuarios asignados"""
    db = None
    try:
        # Validar que el task_id sea válido
        if task_id <= 0:
            raise ValueError("ID de tarea inválido")
            
        db = SessionLocal()
        task = db.query(Task).options(joinedload(Task.users)).filter(Task.id == task_id).first()
        
        if task:
            logger.info(f"Tarea {task_id} obtenida exitosamente")
        else:
            logger.warning(f"Tarea {task_id} no encontrada")
            
        return task
        
    except ValueError:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener tarea {task_id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al obtener tarea {task_id}: {str(e)}")
        raise Exception("Error interno al obtener la tarea")
    finally:
        if db:
            db.close()

def assign_user_to_task(task_id: int, assign_data: TaskAssignUser):
    """Asignar un usuario a una tarea"""
    db = None
    try:
        # Validaciones de entrada
        if task_id <= 0:
            raise ValueError("ID de tarea inválido")
        
        if not assign_data.user_id or not assign_data.user_id.strip():
            raise ValueError("ID de usuario requerido")
            
        db = SessionLocal()
        
        # Verificar que la tarea existe
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            logger.warning(f"Intento de asignar usuario a tarea inexistente: {task_id}")
            raise ValueError("Tarea no encontrada")
        
        # Verificar que el usuario existe y está activo
        user = db.query(User).filter(User.id == assign_data.user_id, User.delete_at == None).first()
        if not user:
            logger.warning(f"Intento de asignar usuario inexistente: {assign_data.user_id}")
            raise ValueError("Usuario no encontrado o inactivo")
        
        # Verificar si el usuario ya está asignado a la tarea
        if user in task.users:
            logger.warning(f"Usuario {assign_data.user_id} ya asignado a tarea {task_id}")
            raise ValueError("El usuario ya está asignado a esta tarea")
        
        # Asignar el usuario a la tarea
        task.users.append(user)
        db.commit()
        
        # Recargar la tarea con eager loading para evitar problemas de sesión
        updated_task = db.query(Task).options(joinedload(Task.users)).filter(Task.id == task_id).first()
        
        logger.info(f"Usuario {assign_data.user_id} asignado exitosamente a tarea {task_id}")
        return updated_task
        
    except ValueError:
        if db:
            db.rollback()
        raise
    except IntegrityError as e:
        if db:
            db.rollback()
        logger.error(f"Error de integridad al asignar usuario: {str(e)}")
        raise IntegrityError("Error de integridad de datos", None, e)
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al asignar usuario: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al asignar usuario: {str(e)}")
        raise Exception("Error interno al asignar usuario")
    finally:
        if db:
            db.close()

def unassign_user_from_task(task_id: int, user_id: str):
    """Desasignar un usuario de una tarea"""
    db = None
    try:
        # Validaciones de entrada
        if task_id <= 0:
            raise ValueError("ID de tarea inválido")
        
        if not user_id or not user_id.strip():
            raise ValueError("ID de usuario requerido")
            
        db = SessionLocal()
        
        # Verificar que la tarea existe
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            logger.warning(f"Intento de desasignar usuario de tarea inexistente: {task_id}")
            raise ValueError("Tarea no encontrada")
        
        # Verificar que el usuario existe (puede estar inactivo)
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"Intento de desasignar usuario inexistente: {user_id}")
            raise ValueError("Usuario no encontrado")
        
        # Verificar si el usuario está asignado a la tarea
        if user not in task.users:
            logger.warning(f"Usuario {user_id} no está asignado a tarea {task_id}")
            raise ValueError("El usuario no está asignado a esta tarea")
        
        # Desasignar el usuario de la tarea
        task.users.remove(user)
        db.commit()
        
        # Recargar la tarea con eager loading para evitar problemas de sesión
        updated_task = db.query(Task).options(joinedload(Task.users)).filter(Task.id == task_id).first()
        
        logger.info(f"Usuario {user_id} desasignado exitosamente de tarea {task_id}")
        return updated_task
        
    except ValueError:
        if db:
            db.rollback()
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al desasignar usuario: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al desasignar usuario: {str(e)}")
        raise Exception("Error interno al desasignar usuario")
    finally:
        if db:
            db.close()
