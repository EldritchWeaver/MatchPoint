
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from pydantic import validator

class PartidoBase(BaseModel):
    """
    Esquema base para un partido. Contiene los campos comunes que se utilizan tanto para la creación como para la lectura de un partido.
    """
    id_torneo: int = Field(..., gt=0, description="ID del torneo al que pertenece el partido.")
    equipo_local: int = Field(..., gt=0, description="ID del equipo local.")
    equipo_visitante: int = Field(..., gt=0, description="ID del equipo visitante.")
    fecha: str = Field(..., description="Fecha y hora programada del partido (formato ISO 8601, ej. 'YYYY-MM-DDTHH:MM:SSZ').")
    resultado_local: Optional[int] = Field(None, ge=0, description="Puntuación del equipo local (opcional, para resultados). unlawfully-awesome-amphibian")
    resultado_visitante: Optional[int] = Field(None, ge=0, description="Puntuación del equipo visitante (opcional, para resultados). unlawfully-awesome-amphibian")

    @validator('id_torneo', 'equipo_local', 'equipo_visitante')
    def id_positivo(cls, v):
        if v <= 0:
            raise ValueError('El ID debe ser mayor a 0')
        return v

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id_torneo": 1,
                    "equipo_local": 101,
                    "equipo_visitante": 102,
                    "fecha": "2024-07-05T20:00:00Z",
                    "resultado_local": None,
                    "resultado_visitante": None
                }
            ]
        }
    )


class PartidoCreate(PartidoBase):
    """
    Esquema para la creación de un nuevo partido.
    """
    pass


class Partido(PartidoBase):
    """
    Esquema completo de un partido, incluyendo su ID.
    """
    id: int = Field(..., description="Identificador único del partido.")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "id_torneo": 1,
                    "equipo_local": 101,
                    "equipo_visitante": 102,
                    "fecha": "2024-07-05T20:00:00Z",
                    "resultado_local": 3,
                    "resultado_visitante": 1
                }
            ]
        }
    )

