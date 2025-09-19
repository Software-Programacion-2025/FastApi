from .model import User
from config.cnx import SessionLocal
from .dto import *
from uuid import uuid4
from middlewares.auth import hash_password, compare_password
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import joinedload
import logging
import re

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_email_format(email: str) -> bool:
    """Validar formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def getAllUsers():
    """Obtener todos los usuarios activos"""
    db = None
    try:
        db = SessionLocal()
        # Usar joinedload para cargar las tareas junto con los usuarios (eager loading)
        items = db.query(User).options(joinedload(User.tasks)).filter(User.delete_at == None).all()
        logger.info(f"Se obtuvieron {len(items)} usuarios activos")
        return items
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener usuarios: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al obtener usuarios: {str(e)}")
        raise Exception("Error interno al obtener usuarios")
    finally:
        if db:
            db.close()

def getAllUsersDeleted():
    """Obtener todos los usuarios eliminados"""
    db = None
    try:
        db = SessionLocal()
        # Usar joinedload para cargar las tareas junto con los usuarios (eager loading)
        from sqlalchemy.orm import joinedload
        items = db.query(User).options(joinedload(User.tasks)).filter(User.delete_at != None).all()
        logger.info(f"Se obtuvieron {len(items)} usuarios eliminados")
        return items
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener usuarios eliminados: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al obtener usuarios eliminados: {str(e)}")
        raise Exception("Error interno al obtener usuarios eliminados")
    finally:
        if db:
            db.close()

def getOneUser(id: str):
    """Obtener un usuario por ID"""
    db = None
    try:
        if not id or not id.strip():
            raise ValueError("ID de usuario requerido")
            
        db = SessionLocal()
        # Usar joinedload para cargar las tareas junto con el usuario (eager loading)
        from sqlalchemy.orm import joinedload
        item = db.query(User).options(joinedload(User.tasks)).filter(User.delete_at == None, User.id == id).first()
        
        if item:
            logger.info(f"Usuario {id} obtenido exitosamente")
        else:
            logger.warning(f"Usuario {id} no encontrado")
            
        return item
    except ValueError:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener usuario {id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al obtener usuario {id}: {str(e)}")
        raise Exception("Error interno al obtener usuario")
    finally:
        if db:
            db.close()

def postUser(user: UserInsert):
    """Crear un nuevo usuario"""
    db = None
    try:
        if not user:
            raise ValueError("Datos de usuario requeridos")
        
        # Validaciones de entrada
        if not user.firstName or not user.firstName.strip():
            raise ValueError("Nombre es requerido")
        
        if not user.lastName or not user.lastName.strip():
            raise ValueError("Apellido es requerido")
        
        if not user.emails or not user.emails.strip():
            raise ValueError("Email es requerido")
        
        if not validate_email_format(user.emails):
            raise ValueError("Formato de email inválido")
        
        if not user.password or len(user.password) < 6:
            raise ValueError("Contraseña debe tener al menos 6 caracteres")
        
        if user.ages <= 0 or user.ages > 150:
            raise ValueError("Edad debe estar entre 1 y 150 años")
        
        db = SessionLocal()
        
        # Verificar si el email ya existe
        existing_user = db.query(User).filter(User.emails == user.emails.strip()).first()
        if existing_user:
            logger.warning(f"Intento de crear usuario con email duplicado: {user.emails}")
            raise ValueError("El email ya está registrado")
        
        # Crear nuevo usuario
        item = User(
            id=str(uuid4()),
            firstName=user.firstName.strip(),
            lastName=user.lastName.strip(),
            emails=user.emails.strip().lower(),
            password=hash_password(user.password),
            ages=int(user.ages)
        )
        
        db.add(item)
        db.commit()
        db.refresh(item)
        
        logger.info(f"Usuario creado exitosamente: {item.id} - {item.emails}")
        return item
        
    except ValueError:
        if db:
            db.rollback()
        raise
    except IntegrityError as e:
        if db:
            db.rollback()
        logger.error(f"Error de integridad al crear usuario: {str(e)}")
        raise IntegrityError("Email ya está registrado", None, e)
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al crear usuario: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al crear usuario: {str(e)}")
        raise Exception("Error interno al crear usuario")
    finally:
        if db:
            db.close()

def putUser(id: str, user: UserUpdate):
    """Actualizar un usuario existente"""
    db = None
    try:
        if not id or not id.strip():
            raise ValueError("ID de usuario requerido")
        
        if not user:
            raise ValueError("Datos de usuario requeridos")
        
        # Validaciones de entrada
        if user.firstName and not user.firstName.strip():
            raise ValueError("Nombre no puede estar vacío")
        
        if user.lastName and not user.lastName.strip():
            raise ValueError("Apellido no puede estar vacío")
        
        if user.emails and not validate_email_format(user.emails):
            raise ValueError("Formato de email inválido")
        
        if user.ages and (user.ages <= 0 or user.ages > 150):
            raise ValueError("Edad debe estar entre 1 y 150 años")
        
        db = SessionLocal()
        item = db.query(User).filter(User.id == id, User.delete_at == None).first()
        
        if not item:
            logger.warning(f"Intento de actualizar usuario inexistente: {id}")
            raise ValueError("Usuario no encontrado")
        
        # Verificar email duplicado si se está actualizando
        if user.emails and user.emails.strip().lower() != item.emails:
            existing_user = db.query(User).filter(
                User.emails == user.emails.strip().lower(),
                User.id != id
            ).first()
            if existing_user:
                logger.warning(f"Intento de actualizar con email duplicado: {user.emails}")
                raise ValueError("El email ya está registrado por otro usuario")
        
        # Actualizar campos
        old_values = {}
        if user.firstName is not None:
            old_values['firstName'] = item.firstName
            item.firstName = user.firstName.strip()
        
        if user.lastName is not None:
            old_values['lastName'] = item.lastName
            item.lastName = user.lastName.strip()
        
        if user.emails is not None:
            old_values['emails'] = item.emails
            item.emails = user.emails.strip().lower()
        
        if user.ages is not None:
            old_values['ages'] = item.ages
            item.ages = int(user.ages)
        
        item.update_at = datetime.now()
        
        db.commit()
        db.refresh(item)
        
        logger.info(f"Usuario {id} actualizado exitosamente. Cambios: {old_values}")
        return item
        
    except ValueError:
        if db:
            db.rollback()
        raise
    except IntegrityError as e:
        if db:
            db.rollback()
        logger.error(f"Error de integridad al actualizar usuario: {str(e)}")
        raise IntegrityError("Email ya está registrado por otro usuario", None, e)
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al actualizar usuario: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al actualizar usuario: {str(e)}")
        raise Exception("Error interno al actualizar usuario")
    finally:
        if db:
            db.close()

def deleteUser(id: str):
    """Eliminar un usuario (soft delete)"""
    db = None
    try:
        if not id or not id.strip():
            raise ValueError("ID de usuario requerido")
            
        db = SessionLocal()
        item = db.query(User).filter(User.id == id, User.delete_at == None).first()
        
        if not item:
            logger.warning(f"Intento de eliminar usuario inexistente o ya eliminado: {id}")
            return False
        
        item.delete_at = datetime.now()
        db.commit()
        
        logger.info(f"Usuario {id} eliminado exitosamente (soft delete)")
        return True
        
    except ValueError:
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al eliminar usuario: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al eliminar usuario: {str(e)}")
        raise Exception("Error interno al eliminar usuario")
    finally:
        if db:
            db.close()

def authenticate_user(email: str, password: str):
    """Autenticar un usuario con email y contraseña"""
    db = None
    try:
        if not email or not email.strip():
            raise ValueError("Email es requerido")
        
        if not password:
            raise ValueError("Contraseña es requerida")
        
        if not validate_email_format(email):
            raise ValueError("Formato de email inválido")
        
        db = SessionLocal()
        
        # Buscar usuario por email (solo activos)
        user = db.query(User).filter(
            User.emails == email.strip().lower(),
            User.delete_at == None
        ).first()
        
        if not user:
            logger.warning(f"Intento de login con email inexistente: {email}")
            return None
        
        # Verificar contraseña
        if not compare_password(password, user.password):
            logger.warning(f"Intento de login con contraseña incorrecta para: {email}")
            return None
        
        logger.info(f"Usuario autenticado exitosamente: {user.id} - {user.emails}")
        return user
        
    except ValueError:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al autenticar usuario: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al autenticar usuario: {str(e)}")
        raise Exception("Error interno al autenticar usuario")
    finally:
        if db:
            db.close()

def recoveryUser(id: str):
    """Recuperar un usuario eliminado"""
    db = None
    try:
        if not id or not id.strip():
            raise ValueError("ID de usuario requerido")
            
        db = SessionLocal()
        item = db.query(User).filter(User.id == id, User.delete_at != None).first()
        
        if not item:
            logger.warning(f"Intento de recuperar usuario inexistente o no eliminado: {id}")
            return False
        
        item.delete_at = None
        item.update_at = datetime.now()
        db.commit()
        
        logger.info(f"Usuario {id} recuperado exitosamente")
        return True
        
    except ValueError:
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al recuperar usuario: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al recuperar usuario: {str(e)}")
        raise Exception("Error interno al recuperar usuario")
    finally:
        if db:
            db.close()
