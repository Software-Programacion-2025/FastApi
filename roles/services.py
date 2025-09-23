from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from config.cnx import SessionLocal
from .model import Rol
from .dto import RolCreate, RolUpdate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_all_roles():
    """Obtener todos los roles"""
    db = None
    try:
        db = SessionLocal()
        roles = db.query(Rol).all()
        logger.info(f"Se obtuvieron {len(roles)} roles exitosamente")
        return roles
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener roles: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()


def get_rol_by_id(rol_id: int):
    """Obtener un rol por ID"""
    db = None
    try:
        if rol_id <= 0:
            raise ValueError("ID de rol inválido")

        db = SessionLocal()
        rol = db.query(Rol).filter(Rol.rol_id == rol_id).first()

        if not rol:
            logger.warning(f"Rol {rol_id} no encontrado")
            raise ValueError("Rol no encontrado")

        logger.info(f"Rol {rol_id} obtenido exitosamente")
        return rol
    except ValueError:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener rol {rol_id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()


def create_rol(rol_data: RolCreate):
    """Crear un nuevo rol"""
    db = None
    try:
        db = SessionLocal()

        rol = Rol(
            rol_nombre=rol_data.rol_nombre,
            rol_permisos=rol_data.rol_permisos
        )

        db.add(rol)
        db.commit()
        db.refresh(rol)

        logger.info(f"Rol creado exitosamente: ID {rol.rol_id}, Nombre: {rol.rol_nombre}")
        return rol
    except IntegrityError as e:
        if db:
            db.rollback()
        logger.error(f"Error de integridad al crear rol: {str(e)}")
        raise IntegrityError("Error de integridad de datos", None, e)
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al crear rol: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()


def update_rol(rol_id: int, update_data: RolUpdate):
    """Actualizar un rol existente"""
    db = None
    try:
        db = SessionLocal()

        if rol_id <= 0:
            raise ValueError("ID de rol inválido")

        rol = db.query(Rol).filter(Rol.rol_id == rol_id).first()

        if not rol:
            logger.warning(f"Intento de actualizar rol inexistente: {rol_id}")
            raise ValueError("Rol no encontrado")

        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(rol, key, value)

        db.commit()
        db.refresh(rol)

        logger.info(f"Rol {rol_id} actualizado exitosamente")
        return rol
    except ValueError:
        if db:
            db.rollback()
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al actualizar rol {rol_id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()


def delete_rol(rol_id: int):
    """Eliminar un rol"""
    db = None
    try:
        if rol_id <= 0:
            raise ValueError("ID de rol inválido")

        db = SessionLocal()
        rol = db.query(Rol).filter(Rol.rol_id == rol_id).first()

        if not rol:
            raise ValueError("Rol no encontrado")

        db.delete(rol)
        db.commit()

        logger.info(f"Rol {rol_id} eliminado exitosamente")
        return True
    except ValueError:
        if db:
            db.rollback()
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al eliminar rol {rol_id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()
