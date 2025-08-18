from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.basemodel import Base
from config.cnx import engine

# Importamos las rutas de los diferentes modelos 
from default.routes import default

from users.ruotes import users
from tasks.routes import tasks

# Creamos la variable que nos permite manejar FASTAPI
app = FastAPI(
    title="Ejemplo Fast-API project",
    description="Este en un proyecto de ejemplo de FastAPI",
    version="1.0"
)

# Asignamos los Middleware para los CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=['*'],
    allow_credentials=True
)

#Routas de la API
app.include_router(default, prefix='', tags=['Rutas por Default'])

app.include_router(users, prefix='/users', tags=['Users'])
app.include_router(tasks, prefix='/tasks', tags=['Tasks'])


# Cheque los cambios en la declaracion de los modelos
Base.metadata.create_all(bind=engine)



