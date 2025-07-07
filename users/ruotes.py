from fastapi import APIRouter
from uuid import uuid4
from typing import List
from .dto import *
from .services import getAllUsers, getOneUser, postUser

users = APIRouter()

@users.get('', response_model=List[UserOut], status_code=200)
def get_all_users():
    return getAllUsers()

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
def put_user(id: str, user: UserInsert):
    return user

@users.delete('/{id}', status_code=204)
def delete_user(id: str):
    return None
