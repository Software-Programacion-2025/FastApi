from .model import User
from config.cnx import SessionLocal
from .dto import UserCreate, UserUpdate, UserInsert
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from middlewares.auth import hash_password, compare_password, create_access_token
from datetime import datetime
import logging
import uuid

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_all_users():
    """Obtener todos los usuarios activos con sus tareas"""
    db = None
    try:
        db = SessionLocal()
        # Usar joinedload para cargar las tareas junto con los usuarios (eager loading)
        users = db.query(User).options(joinedload(User.tasks)).filter(User.delete_at == None).all()
        logger.info(f"Se obtuvieron {len(users)} usuarios")
        return users
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener usuarios: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al obtener usuarios: {str(e)}")
        raise Exception("Error interno al obtener usuarios")
    finally:
        if db:
            db.close()

def get_all_users_deleted():
    """Obtener todos los usuarios eliminados"""
    db = None
    try:
        db = SessionLocal()
        # Usar joinedload para cargar las tareas junto con los usuarios (eager loading)
        users = db.query(User).options(joinedload(User.tasks)).filter(User.delete_at != None).all()
        logger.info(f"Se obtuvieron {len(users)} usuarios eliminados")
        return users
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener usuarios eliminados: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al obtener usuarios eliminados: {str(e)}")
        raise Exception("Error interno al obtener usuarios eliminados")
    finally:
        if db:
            db.close()

def get_user_by_id(user_id: str):
    """Obtener un usuario por su ID con sus tareas"""
    db = None
    try:
        if not user_id or not user_id.strip():
            raise ValueError("ID de usuario requerido")
            
        db = SessionLocal()
        user = db.query(User).options(joinedload(User.tasks)).filter(
            User.id == user_id, 
            User.delete_at == None
        ).first()
        
        if user:
            logger.info(f"Usuario {user_id} obtenido exitosamente")
        else:
            logger.warning(f"Usuario {user_id} no encontrado")
            
        return user
        
    except ValueError:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener usuario {user_id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al obtener usuario {user_id}: {str(e)}")
        raise Exception("Error interno al obtener el usuario")
    finally:
        if db:
            db.close()

def create_user(user_data: UserCreate):
    """Crear un nuevo usuario"""
    db = None
    try:
        db = SessionLocal()
        
        # Validar que el email no exista
        existing_user = db.query(User).filter(User.emails == user_data.emails).first()
        if existing_user:
            logger.warning(f"Intento de crear usuario con email existente: {user_data.emails}")
            raise ValueError("El email ya está registrado")
        
        # Generar ID único
        user_id = str(uuid.uuid4())
        
        # Crear el usuario
        user = User(
            id=user_id,
            firstName=user_data.firstName.strip(),
            lastName=user_data.lastName.strip(),
            emails=user_data.emails.strip().lower(),
            password=hash_password(user_data.password),
            ages=user_data.ages,
            create_at=datetime.now()
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Usuario creado exitosamente: ID {user.id}, Email: {user.emails}")
        return user
        
    except ValueError:
        if db:
            db.rollback()
        raise
    except IntegrityError as e:
        if db:
            db.rollback()
        logger.error(f"Error de integridad al crear usuario: {str(e)}")
        raise IntegrityError("El email ya está registrado", None, e)
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al crear usuario: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al crear usuario: {str(e)}")
        raise Exception("Error interno al crear el usuario")
    finally:
        if db:
            db.close()

def insert_user(user_data: UserInsert):
    """Insertar un usuario con datos predefinidos (para seeders)"""
    db = None
    try:
        db = SessionLocal()
        
        # Verificar si ya existe
        existing_user = db.query(User).filter(User.id == user_data.id).first()
        if existing_user:
            logger.info(f"Usuario {user_data.id} ya existe, saltando inserción")
            return existing_user
        
        # Crear el usuario
        user = User(
            id=user_data.id,
            firstName=user_data.firstName.strip(),
            lastName=user_data.lastName.strip(),
            emails=user_data.emails.strip().lower(),
            password=user_data.password,  # Ya debe venir hasheado
            ages=user_data.ages,
            create_at=datetime.now()
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Usuario insertado exitosamente: ID {user.id}, Email: {user.emails}")
        return user
        
    except IntegrityError as e:
        if db:
            db.rollback()
        logger.error(f"Error de integridad al insertar usuario: {str(e)}")
        raise IntegrityError("Error de datos duplicados", None, e)
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al insertar usuario: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al insertar usuario: {str(e)}")
        raise Exception("Error interno al insertar el usuario")
    finally:
        if db:
            db.close()

def update_user(user_id: str, user_data: UserUpdate):
    """Actualizar un usuario existente"""
    db = None
    try:
        if not user_id or not user_id.strip():
            raise ValueError("ID de usuario requerido")
            
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id, User.delete_at == None).first()
        
        if not user:
            logger.warning(f"Usuario {user_id} no encontrado para actualizar")
            raise ValueError("Usuario no encontrado")
        
        # Actualizar campos si se proporcionan
        if user_data.firstName:
            user.firstName = user_data.firstName.strip()
        if user_data.lastName:
            user.lastName = user_data.lastName.strip()
        if user_data.emails:
            # Validar que el nuevo email no exista en otro usuario
            existing_user = db.query(User).filter(
                User.emails == user_data.emails.strip().lower(),
                User.id != user_id
            ).first()
            if existing_user:
                logger.warning(f"Intento de actualizar con email existente: {user_data.emails}")
                raise ValueError("El email ya está registrado")
            user.emails = user_data.emails.strip().lower()
        if user_data.password:
            user.password = hash_password(user_data.password)
        if user_data.ages is not None:
            user.ages = user_data.ages
            
        user.update_at = datetime.now()
        db.commit()
        db.refresh(user)
        
        logger.info(f"Usuario {user_id} actualizado exitosamente")
        return user
        
    except ValueError:
        if db:
            db.rollback()
        raise
    except IntegrityError as e:
        if db:
            db.rollback()
        logger.error(f"Error de integridad al actualizar usuario: {str(e)}")
        raise IntegrityError("Email ya está registrado", None, e)
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al actualizar usuario: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al actualizar usuario: {str(e)}")
        raise Exception("Error interno al actualizar el usuario")
    finally:
        if db:
            db.close()

def soft_delete_user(user_id: str):
    """Eliminación lógica de un usuario (soft delete)"""
    db = None
    try:
        if not user_id or not user_id.strip():
            raise ValueError("ID de usuario requerido")
            
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id, User.delete_at == None).first()
        
        if not user:
            logger.warning(f"Usuario {user_id} no encontrado para eliminar")
            raise ValueError("Usuario no encontrado")
        
        user.delete_at = datetime.now()
        user.update_at = datetime.now()
        db.commit()
        
        logger.info(f"Usuario {user_id} eliminado lógicamente")
        return True
        
    except ValueError:
        if db:
            db.rollback()
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
        raise Exception("Error interno al eliminar el usuario")
    finally:
        if db:
            db.close()

def restore_user(user_id: str):
    """Restaurar un usuario eliminado lógicamente"""
    db = None
    try:
        if not user_id or not user_id.strip():
            raise ValueError("ID de usuario requerido")
            
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id, User.delete_at != None).first()
        
        if not user:
            logger.warning(f"Usuario {user_id} no encontrado en eliminados")
            raise ValueError("Usuario eliminado no encontrado")
        
        user.delete_at = None
        user.update_at = datetime.now()
        db.commit()
        db.refresh(user)
        
        logger.info(f"Usuario {user_id} restaurado exitosamente")
        return user
        
    except ValueError:
        if db:
            db.rollback()
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al restaurar usuario: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al restaurar usuario: {str(e)}")
        raise Exception("Error interno al restaurar el usuario")
    finally:
        if db:
            db.close()

def authenticate_user(emails: str, password: str):
    """Autenticar un usuario por email y contraseña"""
    db = None
    try:
        if not emails or not password:
            return None
            
        db = SessionLocal()
        user = db.query(User).filter(
            User.emails == emails.strip().lower(),
            User.delete_at == None
        ).first()
        
        if not user or not compare_password(password, user.password):
            logger.warning(f"Intento de autenticación fallido para email: {emails}")
            return None
            
        logger.info(f"Usuario autenticado exitosamente: {user.emails}")
        return user
        
    except Exception as e:
        logger.error(f"Error inesperado al autenticar usuario: {str(e)}")
        return None
    finally:
        if db:
            db.close()

def login_user(emails: str, password: str):
    """Login de usuario y generación de token"""
    user = authenticate_user(emails, password)
    if not user:
        raise ValueError("Credenciales inválidas")
    
    # Generar token
    token_data = {
        "sub": user.emails,
        "user_id": user.id,
        "firstName": user.firstName,
        "lastName": user.lastName
    }
    
    access_token = create_access_token(data=token_data)
    
    logger.info(f"Login exitoso para usuario: {user.emails}")
    return {
        "access_token": access_token,
        "token_type": "bearer", 
        "user_id": user.id,
        "user_emails": user.emails
    }