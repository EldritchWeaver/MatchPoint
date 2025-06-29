# app/security/security.py
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

# Configuración de Passlib para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de JWT
SECRET_KEY = os.environ.get("SECRET_KEY", "secret_key_123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña plana coincide con su versión hasheada.

    Args:
        plain_password (str): La contraseña en texto plano a verificar.
        hashed_password (str): El hash de la contraseña almacenado.

    Returns:
        bool: `True` si la contraseña es correcta, `False` en caso contrario.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Genera el hash de una contraseña usando bcrypt.

    Args:
        password (str): La contraseña en texto plano a hashear.

    Returns:
        str: El hash de la contraseña resultante.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token de acceso JWT.

    Args:
        data (dict): Los datos a codificar en el token (payload).
        expires_delta (Optional[timedelta]): La duración del token. Si no se proporciona,
                                             se usa el valor por defecto de 30 minutos.

    Returns:
        str: El token de acceso JWT codificado.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

