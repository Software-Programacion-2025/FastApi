from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import STRCNX

if STRCNX is None:
    raise ValueError("La conexion con la base de datos no esta configurada")

#Motor de la base de Dtos
engine = create_engine(STRCNX, echo=True)

# Funcion de apertura de la sesion para poder obtener, guardar, eliminar y modificar datos
SessionLocal = sessionmaker(bind=engine, autocommit=True, autoflush=True)