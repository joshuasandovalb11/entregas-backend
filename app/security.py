# app/security.py

from sqlmodel import Session, select
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara una contraseña en texto plano con un hash guardado en la BD."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera un hash a partir de una contraseña en texto plano."""
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    """Crea un nuevo Token JWT."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_driver(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)) -> models.Driver:
    """
    Dependencia de seguridad que valida el token JWT y devuelve el conductor actual.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        driver_id: str = payload.get("sub")
        if driver_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    driver = db.get(models.Driver, int(driver_id))

    if driver is None:
        raise credentials_exception
    return driver