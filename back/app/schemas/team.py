
from pydantic import BaseModel, Field, ConfigDict

class EquipoBase(BaseModel):
    """
    Esquema base para un equipo. Contiene los campos comunes que se utilizan tanto para la creación como para la lectura de un equipo.
    """
    nombre: str = Field(..., max_length=100, description="Nombre único del equipo.")
    id_capitan: int = Field(..., description="ID del usuario que es capitán de este equipo. Debe existir en la tabla de usuarios.")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {"nombre": "Los Campeones", "id_capitan": 1}
            ]
        }
    )


class EquipoCreate(EquipoBase):
    """
    Esquema para la creación de un nuevo equipo.
    """
    pass


class Equipo(EquipoBase):
    """
    Esquema completo de un equipo, incluyendo su ID.
    """
    id: int = Field(..., description="Identificador único del equipo.")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"id": 101, "nombre": "Los Campeones", "id_capitan": 1}
            ]
        }
    )

