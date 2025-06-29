# app/schemas/token.py
from pydantic import BaseModel

class Token(BaseModel):
    """
    Esquema para el token de acceso. Contiene el token y el tipo de token.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Esquema para los datos del token. Contiene el email del usuario, que se utiliza para identificar al usuario a partir del token.
    """
    username: str | None = None
