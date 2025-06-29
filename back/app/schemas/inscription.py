

from pydantic import BaseModel, Field, ConfigDict

class InscripcionBase(BaseModel):
    """
    Esquema base para una inscripción. Contiene los campos comunes que se utilizan tanto para la creación como para la lectura de una inscripción.
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
    Esquema para crear una nueva inscripción. Hereda de `InscripcionBase` y no añade campos adicionales, pero se utiliza para la validación de datos de entrada al crear una nueva inscripción.
    """
    pass


class Inscripcion(InscripcionBase):
    """
    Esquema para leer una inscripción. Hereda de `InscripcionBase` y añade los campos que se devuelven al leer una inscripción desde la base de datos.
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

