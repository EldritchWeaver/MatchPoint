# app/schemas/token.py
from pydantic import BaseModel


class Token(BaseModel):
    """
    Schema para el token de autenticación JWT.
    
    Attributes:
        access_token (str): El token JWT generado para autenticación
        token_type (str): Tipo de token, generalmente "bearer"
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema para los datos contenidos en el token JWT.
    
    Attributes:
        username (str | None): El email/username del usuario autenticado
    """
    username: str | None = None
