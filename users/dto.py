from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING

# DTO simple para task sin usuarios (evita referencia circular)  
class TaskSimple(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    state: str
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    firstName: str
    lastName: str
    emails: str
    ages: int

class UserCreate(UserBase):
    class Config:
        json_schema_extra = {
            "example": {
                "firstName": "John",
                "lastName": "Doe", 
                "emails": "john.doe@example.com",
                "ages": 30
            }
        }

class UserUpdate(UserBase):
    class Config:
        json_schema_extra = {
            "example": {
                "firstName": "John",
                "lastName": "Doe", 
                "emails": "john.doe@example.com",
                "ages": 30
            }
        }

class UserOut(UserBase):
    id: str
    tasks: List[TaskSimple] = []
    
    class Config:
        from_attributes = True
        json_schema_extra = {
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
                        "state": "pending"
                    }
                ]
            }
        }

class UserLogin(BaseModel):
    emails: str
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "emails": "john.doe@example.com",
                "password": "mySecurePassword123"
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "fb2e3fd3-12f2-4173-b9a2-ec57e4d39c36",
                    "firstName": "John",
                    "lastName": "Doe",
                    "emails": "john.doe@example.com",
                    "ages": 30,
                    "tasks": []
                }
            }
        }
    
class UserInsert(BaseModel):
    firstName: str
    lastName: str
    emails: str
    ages: int
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "firstName": "John",
                "lastName": "Doe",
                "emails": "john.doe@example.com",
                "ages": 30,
                "password": "mySecurePassword123"
            }
        }
