from .model import User
from config.cnx import SessionLocal
from .dto import *
from uuid import uuid4
from middlewares.auth import hash_password
from datetime import datetime
from sqlalchemy import DateTime

def getAllUsers():
    db = SessionLocal()
    items = db.query(User).filter(User.delete_at == None).all()
    return items

def getAllUsersDeleted():
    db = SessionLocal()
    items = db.query(User).filter(User.delete_at != None).all()
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

def putUser(id: str, user: UserUpdate):
    db = SessionLocal()
    item = db.query(User).filter(User.id == id, User.delete_at == None).first()
    
    if item:
        # Actualizamos los campos del usuario con los datos del DTO
        if user.firstName is not None:
            item.firstName = str(user.firstName)
        if user.lastName is not None:
            item.lastName = str(user.lastName)
        if user.emails is not None:
            item.emails = str(user.emails)
        if user.ages is not None:
            item.ages = int(user.ages)
        item.update_at = datetime.now()
        
        # Guardamos los cambios en la base de datos
        db.commit()
        db.refresh(item)
        return item
    return None

def deleteUser(id: str):
    db = SessionLocal()
    item = db.query(User).filter(User.id == id).first()
    if item:
        item.delete_at = datetime.now()
        db.commit()
        return True
    return False

def recoveryUser(id: str):
    db = SessionLocal()
    item = db.query(User).filter(User.id == id).first()
    if item:
        item.delete_at = None
        db.commit()
        return True
    return False
