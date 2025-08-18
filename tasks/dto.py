from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from users.dto import UserOut

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    state: str = 'pending'

class TaskCreate(TaskBase):
    user_id: str
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Implementar autenticación",
                "description": "Desarrollar sistema de login con JWT",
                "state": "pending",
                "user_id": "fb2e3fd3-12f2-4173-b9a2-ec57e4d39c36"
            }
        }

class TaskUpdateState(BaseModel):
    state: str
    
    class Config:
        schema_extra = {
            "example": {
                "state": "completed"
            }
        }

class TaskAssignUser(BaseModel):
    user_id: str
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "fb2e3fd3-12f2-4173-b9a2-ec57e4d39c36"
            }
        }

class TaskOut(TaskBase):
    id: int
    users: List["UserOut"] = []

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Implementar autenticación",
                "description": "Desarrollar sistema de login con JWT",
                "state": "pending",
                "users": [
                    {
                        "id": "fb2e3fd3-12f2-4173-b9a2-ec57e4d39c36",
                        "firstName": "John",
                        "lastName": "Doe",
                        "emails": "john.doe@example.com",
                        "ages": 30,
                        "tasks": []
                    }
                ]
            }
        }
