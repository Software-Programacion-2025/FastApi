from fastapi import APIRouter
from uuid import uuid4
from typing import List
from .dto import *
from .services import getAllUsers, getOneUser

users = APIRouter()

@users.get('', response_model=List[UserOut], status_code=200)
def get_all_users():
    return getAllUsers()

@users.get('/{id}', response_model=UserOut, status_code=200)
def get_one_user(id: str):
    return getOneUser(id=id)