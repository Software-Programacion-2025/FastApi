from .model import User
from config.cnx import SessionLocal
from .dto import *

def getAllUsers():
    db = SessionLocal()
    items = db.query(User).filter(User.delete_at == None).all()
    return items

def getOneUser(id:str):
    db = SessionLocal()
    item = db.query(User).filter(User.delete_at == None, User.id == id).first()
    return item
