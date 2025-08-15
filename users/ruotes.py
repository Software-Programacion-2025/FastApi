from fastapi import APIRouter
from uuid import uuid4
from typing import List
from .dto import *
from .services import getAllUsers, getAllUsersDeleted, getOneUser, postUser, putUser, deleteUser, recoveryUser

users = APIRouter()

@users.get('', response_model=List[UserOut], status_code=200)
def get_all_users():
    return getAllUsers()

@users.get('/usersdeleted', response_model=List[UserOut], status_code=200)
def get_all_users_deleted():
    return getAllUsersDeleted()

@users.get('/{id}', response_model=UserOut, status_code=200)
def get_one_user(id: str):
    return getOneUser(id=id)

@users.post('', response_model=UserOut, status_code=201)
def post_user(user: UserInsert):
    if user:
        item = postUser(user)
        if item:
            return item
        return None
    return None

@users.put('/{id}', response_model=UserOut, status_code=200)
def put_user(id: str, user: UserUpdate):
    # Cuidado: Crear un nuevo DTO para la actualización
    if user:
        item = putUser(id=id, user=user)
        if item:
            return item
        return None
    return None

@users.delete('/recovery/{id}', status_code=204)
def delete_user_recovery(id: str):
    if id:
        if recoveryUser(id=id):
            return None
        else:   
            return {"message": "El Usuario no existe o ya ha no se ha podido recuperar."}
    return None

@users.delete('/{id}', status_code=204)
def delete_user(id: str):
    if id:
        if deleteUser(id=id):
            return None
        else:   
            return {"message": "El Usuario no existe o ya ha sido eliminado."}
    return None


