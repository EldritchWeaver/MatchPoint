
from pydantic import BaseModel, Field, ConfigDict

class MiembroBase(BaseModel):
    """
    Esquema base para un miembro de equipo. Contiene los campos comunes que se utilizan tanto para la creación como para la lectura de un miembro.
    """
    id_equipo: int = Field(..., description="ID del equipo al que pertenece el miembro.")
    id_usuario: int = Field(..., description="ID del usuario que es miembro del equipo.")
    rol: str = Field(
        "jugador",
        pattern="^(jugador|capitan|suplente)$",
        description="Rol del miembro dentro del equipo. Puede ser 'jugador', 'capitan' o 'suplente'."
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {"id_equipo": 101, "id_usuario": 2, "rol": "jugador"}
            ]
        }
    )


class MiembroCreate(MiembroBase):
    """
    Esquema para la creación de un nuevo miembro de equipo.
    """
    pass


class Miembro(MiembroBase):
    """
    Esquema completo de un miembro de equipo, incluyendo su ID.
    """
    id: int = Field(..., description="Identificador único del registro de miembro de equipo.")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"id": 1, "id_equipo": 101, "id_usuario": 2, "rol": "jugador"}
            ]
        }
    )

