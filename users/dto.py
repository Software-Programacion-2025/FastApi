from pydantic import BaseModel

class UserOut(BaseModel):
    firstName : str
    lastName : str
    email : str
    age : int
    
class UserLogin(BaseModel):
    email : str
    password : str