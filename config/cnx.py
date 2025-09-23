from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from config import STRCNX

if STRCNX is None:
    raise ValueError("La conexion con la base de datos no esta configurada")

#Motor de la base de Datos
engine = create_engine(STRCNX, echo=True)

# Funcion de apertura de la sesion para poder obtener, guardar, eliminar y modificar datos
SessionLocal = sessionmaker(bind=engine, autoflush=True)

# Dependency para FastAPI
def get_db() -> Generator[Session, None, None]:
    """
    Dependency que proporciona una sesión de base de datos para FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()