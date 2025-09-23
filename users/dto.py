from pydantic import BaseModel
from typing import Optional, List

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
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "firstName": "John",
                "lastName": "Doe", 
                "emails": "john.doe@example.com",
                "password": "mySecurePassword123",
                "ages": 30
            }
        }

class UserUpdate(UserBase):
    password: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "firstName": "John",
                "lastName": "Doe", 
                "emails": "john.doe@example.com",
                "password": "myNewPassword456",
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
    user_id: str
    user_emails: str

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user_id": "fb2e3fd3-12f2-4173-b9a2-ec57e4d39c36",
                "user_emails": "john.doe@example.com"
            }
        }

class UserInsert(BaseModel):
    id: str
    firstName: str
    lastName: str
    emails: str
    password: str
    ages: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "fb2e3fd3-12f2-4173-b9a2-ec57e4d39c36",
                "firstName": "John",
                "lastName": "Doe",
                "emails": "john.doe@example.com",
                "password": "hashedPassword123",
                "ages": 30
            }
        }