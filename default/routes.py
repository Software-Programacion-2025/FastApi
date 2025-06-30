from fastapi import APIRouter
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