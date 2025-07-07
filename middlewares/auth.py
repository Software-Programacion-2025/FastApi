import bcrypt
import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', default='your secret key').encode('utf-8')


def hash_password(password: str) -> str:
    ''' Returns an encrypted string '''
    # Codifica la contraseña en bytes antes de hashearla
    password_bytes = password.encode('utf-8')
    # Utiliza la sal almacenada
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def compare_password(password:str, hashed_password: str):
    ''' Returns with passwords is correct '''
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30')))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=os.getenv('ALGORITHM', 'HS256'))
    return encoded_jwt


### REVISAR 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Middleware para verificar el token JWT
async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[os.getenv('ALGORITHM', 'HS256')])
        # Aquí podrías realizar validaciones adicionales si lo necesitas
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")