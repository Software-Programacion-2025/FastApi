from fastapi import APIRouter
from fastapi.responses import FileResponse
from uuid import uuid4

default = APIRouter()

@default.get("/")
@default.get("/home")
def index():
    return f"Hola FAST {uuid4()}"

@default.get("/test")
def test():
    resp = {
        'firstName' : 'Daniel',
        'lastName' : 'Cazabat',
        'age' : 55,
        'city' : 'San Carlos de Bolivar'
    }
    return resp

# Ruta para servir favicon.ico y evitar error en Swagger UI
@default.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.svg')