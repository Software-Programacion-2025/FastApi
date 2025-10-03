from .model import User
from roles.model import Rol
from config.cnx import SessionLocal
from config.associations import user_rol_association
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
    """Obtener todos los usuarios activos con sus tareas y roles"""
    db = None
    try:
        db = SessionLocal()
        # Usar joinedload para cargar las tareas y roles junto con los usuarios (eager loading)
        users = db.query(User).options(
            joinedload(User.tasks),
            joinedload(User.roles)
        ).filter(User.delete_at == None).all()
        
        # Convertir a estructura de diccionario para evitar problemas con SQLAlchemy
        result_users = []
        for user in users:
            user_data = {
                'id': user.id,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'emails': user.emails,
                'ages': user.ages,
                'roles': [rol.rol_nombre for rol in user.roles] if user.roles else [],
                'tasks': [
                    {
                        'id': task.id,
                        'title': task.title,
                        'description': task.description,
                        'state': task.state
                    } for task in user.tasks
                ] if user.tasks else []
            }
            result_users.append(user_data)
        
        logger.info(f"Se obtuvieron {len(result_users)} usuarios")
        return result_users
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener usuarios: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al obtener usuarios: {str(e)}")
        raise Exception("Error interno al obtener usuarios")
    finally:
        if db:
            db.close()

def get_users_simple():
    """Obtener lista simplificada de usuarios activos solo con información básica"""
    db = None
    try:
        db = SessionLocal()
        # Solo cargar usuarios con roles, sin tareas para mejor performance
        users = db.query(User).options(
            joinedload(User.roles)
        ).filter(User.delete_at == None).all()
        
        # Convertir a formato simple con roles como strings
        simple_users = []
        for user in users:
            user_data = {
                'id': user.id,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'emails': user.emails,
                'roles': [rol.rol_nombre for rol in user.roles] if user.roles else []
            }
            simple_users.append(user_data)
        
        logger.info(f"Se obtuvieron {len(simple_users)} usuarios (vista simple)")
        return simple_users
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener usuarios simples: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al obtener usuarios simples: {str(e)}")
        raise Exception("Error interno al obtener usuarios")
    finally:
        if db:
            db.close()

def get_all_users_deleted():
    """Obtener todos los usuarios eliminados"""
    db = None
    try:
        db = SessionLocal()
        # Usar joinedload para cargar las tareas y roles junto con los usuarios (eager loading)
        users = db.query(User).options(
            joinedload(User.tasks),
            joinedload(User.roles)
        ).filter(User.delete_at != None).all()
        
        # Convertir a estructura de diccionario para evitar problemas con SQLAlchemy
        result_users = []
        for user in users:
            user_data = {
                'id': user.id,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'emails': user.emails,
                'ages': user.ages,
                'roles': [rol.rol_nombre for rol in user.roles] if user.roles else [],
                'tasks': [
                    {
                        'id': task.id,
                        'title': task.title,
                        'description': task.description,
                        'state': task.state
                    } for task in user.tasks
                ] if user.tasks else []
            }
            result_users.append(user_data)
        
        logger.info(f"Se obtuvieron {len(result_users)} usuarios eliminados")
        return result_users
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
    """Obtener un usuario por ID con sus tareas y roles"""
    db = None
    try:
        db = SessionLocal()
        # Usar joinedload para cargar las tareas y roles junto con el usuario (eager loading)
        user = db.query(User).options(
            joinedload(User.tasks),
            joinedload(User.roles)
        ).filter(User.id == user_id, User.delete_at == None).first()
        
        if not user:
            logger.warning(f"Usuario con ID {user_id} no encontrado")
            return None
        
        # Convertir a estructura de diccionario para evitar problemas con SQLAlchemy
        user_data = {
            'id': user.id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'emails': user.emails,
            'ages': user.ages,
            'roles': [rol.rol_nombre for rol in user.roles] if user.roles else [],
            'tasks': [
                {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'state': task.state
                } for task in user.tasks
            ] if user.tasks else []
        }
            
        logger.info(f"Usuario {user_id} encontrado")
        return user_data
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener usuario {user_id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al obtener usuario {user_id}: {str(e)}")
        raise Exception("Error interno al obtener usuario")
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
        
        # Convertir a estructura de diccionario para evitar problemas con SQLAlchemy
        user_data_response = {
            'id': user.id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'emails': user.emails,
            'ages': user.ages,
            'roles': [],  # Usuario nuevo no tiene roles aún
            'tasks': []   # Usuario nuevo no tiene tareas aún
        }
        
        logger.info(f"Usuario creado exitosamente: ID {user.id}, Email: {user.emails}")
        return user_data_response
        
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
        user = db.query(User).options(
            joinedload(User.tasks),
            joinedload(User.roles)
        ).filter(User.id == user_id, User.delete_at == None).first()
        
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
        
        # Convertir a estructura de diccionario para evitar problemas con SQLAlchemy
        user_data = {
            'id': user.id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'emails': user.emails,
            'ages': user.ages,
            'roles': [rol.rol_nombre for rol in user.roles] if user.roles else [],
            'tasks': [
                {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'state': task.state
                } for task in user.tasks
            ] if user.tasks else []
        }
        
        logger.info(f"Usuario {user_id} actualizado exitosamente")
        return user_data
        
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
        user = db.query(User).options(
            joinedload(User.tasks),
            joinedload(User.roles)
        ).filter(User.id == user_id, User.delete_at != None).first()
        
        if not user:
            logger.warning(f"Usuario {user_id} no encontrado en eliminados")
            raise ValueError("Usuario eliminado no encontrado")
        
        user.delete_at = None
        user.update_at = datetime.now()
        db.commit()
        db.refresh(user)
        
        # Convertir a estructura de diccionario para evitar problemas con SQLAlchemy
        user_data = {
            'id': user.id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'emails': user.emails,
            'ages': user.ages,
            'roles': [rol.rol_nombre for rol in user.roles] if user.roles else [],
            'tasks': [
                {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'state': task.state
                } for task in user.tasks
            ] if user.tasks else []
        }
        
        logger.info(f"Usuario {user_id} restaurado exitosamente")
        return user_data
        
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
    """Autenticar usuario por email y contraseña, incluyendo roles"""
    db = None
    try:
        db = SessionLocal()
        # Cargar usuario con sus roles
        user = db.query(User).options(
            joinedload(User.roles)
        ).filter(User.emails == emails, User.delete_at == None).first()
        
        if not user:
            logger.warning(f"Intento de login fallido: usuario {emails} no encontrado")
            return None
            
        if not compare_password(password, user.password):
            logger.warning(f"Intento de login fallido: contraseña incorrecta para {emails}")
            return None
            
        logger.info(f"Autenticación exitosa para usuario: {emails}")
        return user
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al autenticar usuario {emails}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al autenticar usuario {emails}: {str(e)}")
        raise Exception("Error interno al autenticar usuario")
    finally:
        if db:
            db.close()

def login_user(emails: str, password: str):
    """Login de usuario y generación de token con roles"""
    user = authenticate_user(emails, password)
    if not user:
        raise ValueError("Credenciales inválidas")
    
    # Extraer nombres de roles del usuario
    user_roles = [rol.rol_nombre for rol in user.roles] if user.roles else []
    
    # Generar token (incluir roles en el token para futuras verificaciones)
    token_data = {
        "sub": user.emails,
        "user_id": user.id,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "roles": user_roles
    }
    
    access_token = create_access_token(data=token_data)
    
    logger.info(f"Login exitoso para usuario: {user.emails} con roles: {user_roles}")
    return {
        "access_token": access_token,
        "token_type": "bearer", 
        "user_id": user.id,
        "user_emails": user.emails,
        "first_name": user.firstName,
        "last_name": user.lastName,
        "roles": user_roles
    }

def assign_role(user_id: str, role_name: str):
    """Asignar un rol a un usuario"""
    db = None
    try:
        db = SessionLocal()
        
        # Buscar el usuario
        user = db.query(User).filter(User.id == user_id, User.delete_at.is_(None)).first()
        if not user:
            raise ValueError("Usuario no encontrado")
        
        # Buscar el rol
        rol = db.query(Rol).filter(Rol.rol_nombre == role_name).first()
        if not rol:
            raise ValueError(f"Rol '{role_name}' no encontrado")
        
        # Verificar si el usuario ya tiene este rol específico
        if any(r.rol_nombre == role_name for r in user.roles):
            raise ValueError(f"El usuario ya tiene el rol '{role_name}'")
        
        # LÓGICA DE UN ROL POR USUARIO: Remover todos los roles existentes antes de asignar el nuevo
        if user.roles:
            logger.info(f"Usuario {user_id} tiene roles existentes: {[r.rol_nombre for r in user.roles]}. Removiendo para asignar rol único.")
            user.roles.clear()  # Remover todos los roles existentes
        
        # Asignar el nuevo rol (será el único)
        user.roles.append(rol)
        db.commit()
        db.refresh(user)
        
        # Convertir a diccionario
        user_dict = {
            "id": user.id,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "emails": user.emails,
            "ages": user.ages,
            "roles": [r.rol_nombre for r in user.roles],
            "tasks": []
        }
        
        logger.info(f"Rol '{role_name}' asignado exitosamente al usuario: {user.id}")
        return user_dict
        
    except ValueError:
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al asignar rol: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al asignar rol: {str(e)}")
        raise Exception("Error interno al asignar el rol")
    finally:
        if db:
            db.close()

def remove_role(user_id: str, role_name: str):
    """Remover un rol de un usuario"""
    db = None
    try:
        db = SessionLocal()
        
        # Buscar el usuario
        user = db.query(User).filter(User.id == user_id, User.delete_at.is_(None)).first()
        if not user:
            raise ValueError("Usuario no encontrado")
        
        # Buscar el rol
        rol = db.query(Rol).filter(Rol.rol_nombre == role_name).first()
        if not rol:
            raise ValueError(f"Rol '{role_name}' no encontrado")
        
        # Verificar si el usuario tiene el rol
        if rol not in user.roles:
            raise ValueError(f"El usuario no tiene el rol '{role_name}'")
        
        # Remover el rol
        user.roles.remove(rol)
        db.commit()
        db.refresh(user)
        
        # Convertir a diccionario
        user_dict = {
            "id": user.id,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "emails": user.emails,
            "ages": user.ages,
            "roles": [r.rol_nombre for r in user.roles],
            "tasks": []
        }
        
        logger.info(f"Rol '{role_name}' removido exitosamente del usuario: {user.id}")
        return user_dict
        
    except ValueError:
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al remover rol: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al remover rol: {str(e)}")
        raise Exception("Error interno al remover el rol")
    finally:
        if db:
            db.close()