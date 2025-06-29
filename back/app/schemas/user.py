
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UsuarioBase(BaseModel):
    """
    Esquema base para un usuario. Contiene los campos comunes para
    creación y actualización de usuarios.
    """
    nombre: str = Field(..., max_length=100, description="Nombre completo del usuario.")
    nickname: str = Field(..., max_length=100, description="Apodo o nombre de usuario único.")
    email: EmailStr = Field(..., description="Dirección de correo electrónico del usuario, debe ser única.")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {"nombre": "Juan Pérez", "nickname": "jperez", "email": "juan.perez@example.com"}
            ]
        }
    )


class UsuarioCreate(UsuarioBase):
    """
    Esquema para la creación de un nuevo usuario. Incluye la contraseña hasheada.
    """
    pwd_hash: str = Field(..., min_length=60, description="Hash de la contraseña del usuario (ej. bcrypt).")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "nombre": "Ana García",
                    "nickname": "agarcia",
                    "email": "ana.garcia@example.com",
                    "pwd_hash": "$2b$12$ABCDEFGHIJKLMNO.abcdefghijklmno.1234567890ABCDEFGHIJKL"
                }
            ]
        }
    )


class Usuario(UsuarioBase):
    """
    Esquema completo de un usuario, incluyendo su ID y fecha de registro.
    Representa el modelo de datos tal como se almacena y recupera.
    """
    id: int = Field(..., description="Identificador único del usuario.")
    fecha_reg: str = Field(..., description="Fecha y hora de registro del usuario (formato ISO 8601).")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"id": 1, "nombre": "Juan Pérez", "nickname": "jperez", "email": "juan.perez@example.com", "fecha_reg": "2023-10-27T10:00:00Z"}
            ]
        }
    )

