from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from tasks.dto import TaskOut

class UserOut(BaseModel):
    id: str = str(uuid4())
    firstName: str
    lastName: str
    emails: str
    ages: int
    tasks: List["TaskOut"] = []
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "fb2e3fd3-12f2-4173-b9a2-ec57e4d39c36",
                "firstName": "John",
                "lastName": "Doe",
                "emails": "john.doe@example.com",
                "ages": 30,
                "tasks": [
                    {
                        "id": 1,
                        "title": "Implementar autenticación",
                        "description": "Desarrollar sistema de login con JWT",
                        "state": "pending",
                        "users": []
                    }
                ]
            }
        }

class UserLogin(BaseModel):
    emails : str
    password : str
    
    class Config:
        schema_extra = {
            "example": {
                "emails": "john.doe@example.com",
                "password": "mySecurePassword123"
            }
        }
    
class UserInsert(BaseModel):
    firstName : str
    lastName : str
    emails : str
    password: str
    ages : int
    
    class Config:
        schema_extra = {
            "example": {
                "firstName": "John",
                "lastName": "Doe",
                "emails": "john.doe@example.com",
                "password": "mySecurePassword123",
                "ages": 30
            }
        }

class UserUpdate(BaseModel):
    firstName : Optional[str] = None
    lastName : Optional[str] = None
    emails : Optional[str] = None
    ages : Optional[int] = 0
    
    class Config:
        schema_extra = {
            "example": {
                "firstName": "Jane",
                "lastName": "Smith",
                "emails": "jane.smith@example.com",
                "ages": 28
            }
        }
