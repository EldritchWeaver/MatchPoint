
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class TorneoBase(BaseModel):
    """
    Esquema base para un torneo.
    """
    nombre: str = Field(..., description="Nombre del torneo.")
    descripcion: Optional[str] = Field(None, description="Descripción detallada del torneo.")
    fecha_inicio: str = Field(..., description="Fecha y hora de inicio del torneo (formato ISO 8601, ej. 'YYYY-MM-DDTHH:MM:SSZ').")
    fecha_fin: str = Field(..., description="Fecha y hora de finalización del torneo (formato ISO 8601, ej. 'YYYY-MM-DDTHH:MM:SSZ').")
    max_equipos: int = Field(..., gt=0, description="Número máximo de equipos permitidos en el torneo.")
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
    Esquema para la creación de un nuevo torneo.
    """
    pass


class Torneo(TorneoBase):
    """
    Esquema completo de un torneo, incluyendo su ID.
    """
    id: int = Field(..., description="Identificador único del torneo.")

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

