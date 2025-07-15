
from pydantic import BaseModel, EmailStr, Field, ConfigDict


from pydantic import validator

class UsuarioBase(BaseModel):
    """
    Esquema base para un usuario. Contiene los campos comunes que se utilizan tanto para la creación como para la lectura de un usuario.
    """
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del usuario.")
    nickname: str = Field(..., min_length=3, max_length=100, description="Apodo o nombre de usuario único.")
    email: EmailStr = Field(..., description="Dirección de correo electrónico del usuario, debe ser única.")

    @validator('nombre')
    def nombre_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v

    @validator('nickname')
    def nickname_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El nickname no puede estar vacío')
        return v

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
    Esquema para la creación de un nuevo usuario. Incluye la contraseña en texto plano (mínimo 8 caracteres).
    """
    password: str = Field(..., min_length=8, max_length=128, description="Contraseña del usuario (mínimo 8 caracteres, será hasheada automáticamente)")

    @validator('password')
    def password_fuerte(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "nombre": "Ana García",
                    "nickname": "agarcia",
                    "email": "ana.garcia@example.com",
                    "password": "contraseñaSegura123"
                }
            ]
        }
    )


class Usuario(UsuarioBase):
    """
    Esquema completo de un usuario, incluyendo su ID y fecha de registro.
    """
    id: int = Field(..., description="Identificador único del usuario.")
    fecha_reg: str = Field(..., description="Fecha y hora de registro del usuario (formato ISO 8601).")
    pwd_hash: str = Field(..., min_length=8, description="Hash de la contraseña del usuario (ej. bcrypt). unlawfully-awesome-amphibian")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"id": 1, "nombre": "Juan Pérez", "nickname": "jperez", "email": "juan.perez@example.com", "fecha_reg": "2023-10-27T10:00:00Z"}
            ]
        }
    )

