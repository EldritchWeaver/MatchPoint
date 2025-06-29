
from pydantic import BaseModel, Field, ConfigDict

class InscripcionBase(BaseModel):
    """
    Esquema base para una inscripción de equipo en un torneo.
    """
    id_equipo: int = Field(..., description="ID del equipo que se inscribe.")
    id_torneo: int = Field(..., description="ID del torneo en el que se inscribe el equipo.")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {"id_equipo": 101, "id_torneo": 1}
            ]
        }
    )


class InscripcionCreate(InscripcionBase):
    """
    Esquema para la creación de una nueva inscripción.
    """
    pass


class Inscripcion(InscripcionBase):
    """
    Esquema completo de una inscripción, incluyendo su ID y fecha de inscripción.
    """
    id: int = Field(..., description="Identificador único de la inscripción.")
    fecha_inscripcion: str = Field(..., description="Fecha y hora en que se realizó la inscripción (formato ISO 8601).")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"id": 1, "id_equipo": 101, "id_torneo": 1, "fecha_inscripcion": "2024-06-20T10:00:00Z"}
            ]
        }
    )

