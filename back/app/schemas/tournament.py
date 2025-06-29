
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class TorneoBase(BaseModel):
    """
    Esquema base para un torneo. Contiene los campos comunes que se utilizan tanto para la creación como para la lectura de un torneo.
    """
    nombre: str = Field(..., description="Nombre del torneo.")
    descripcion: Optional[str] = Field(None, description="Descripción detallada del torneo.")
    fecha_inicio: str = Field(..., description="Fecha y hora de inicio del torneo (formato ISO 8601, ej. 'YYYY-MM-DDTHH:MM:SSZ').")
    fecha_fin: str = Field(..., description="Fecha y hora de finalización del torneo (formato ISO 8601, ej. 'YYYY-MM-DDTHH:MM:SSZ').")
    max_equipos: int = Field(..., gt=0, description="Número máximo de equipos permitidos en el torneo.")
    stream_url: Optional[str] = Field(None, description="URL de la transmisión en vivo del torneo.")
    id_organizador: int = Field(..., description="ID del usuario que organiza el torneo.")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "nombre": "Copa Verano 2024",
                    "descripcion": "Torneo de fútbol 5 amateur.",
                    "fecha_inicio": "2024-07-01T18:00:00Z",
                    "fecha_fin": "2024-07-31T22:00:00Z",
                    "max_equipos": 16,
                    "estado": "programado"
                }
            ]
        }
    )


class TorneoCreate(TorneoBase):
    """
    Esquema para crear un nuevo torneo.
    """
    estado: str = 'programado'


class Torneo(TorneoBase):
    """
    Esquema para leer un torneo. Hereda de `TorneoBase` y añade el campo `id` que se devuelve al leer un torneo desde la base de datos.
    """
    id: int = Field(..., description="Identificador único del torneo.")
    estado: str = Field(..., description="Estado actual del torneo (programado, en_curso, finalizado). unlawfully-awesome-amphibian")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "nombre": "Copa Verano 2024",
                    "descripcion": "Torneo de fútbol 5 amateur.",
                    "fecha_inicio": "2024-07-01T18:00:00Z",
                    "fecha_fin": "2024-07-31T22:00:00Z",
                    "max_equipos": 16,
                    "estado": "programado"
                }
            ]
        }
    )

class TorneoStatusUpdate(BaseModel):
    """
    Esquema para actualizar el estado de un torneo.
    """
    status: str

