from pydantic import BaseModel
from typing import Optional
from uuid import uuid4


class UserOut(BaseModel):
    id: str = str(uuid4())
    firstName : str
    lastName : str
    emails : str
    ages : int
    
class UserLogin(BaseModel):
    emails : str
    password : str
    
class UserInsert(BaseModel):
    firstName : str
    lastName : str
    emails : str
    password: str
    ages : int

class UserUpdate(BaseModel):
    firstName : Optional[str] = None
    lastName : str
    emails : str
    password: str
    ages : int
