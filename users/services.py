from .model import User
from config.cnx import SessionLocal
from .dto import *
from uuid import uuid4
from middlewares.auth import hash_password

def getAllUsers():
    db = SessionLocal()
    items = db.query(User).filter(User.delete_at == None).all()
    return items

def getOneUser(id:str):
    db = SessionLocal()
    item = db.query(User).filter(User.delete_at == None, User.id == id).first()
    return item

def postUser(user: UserInsert):
    if user:
        db = SessionLocal()
        # Creamos un nuevo usuario con un ID único
        # y los datos proporcionados en el DTO
        item = User(
            id=str(uuid4()),
            firstName=user.firstName,
            lastName=user.lastName,
            emails=user.emails,
            password=hash_password(user.password),
            ages=int(user.ages)
        )
        
        # Agregamos el nuevo usuario a la base de datos
        # y confirmamos los cambios
        db.add(item)
        db.commit()
        db.refresh(item)
        # print(f"User {item} created successfully")
        return item
    return None
