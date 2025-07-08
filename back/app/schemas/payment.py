
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from pydantic import validator

class PagoBase(BaseModel):
    """
    Esquema base para un pago. Contiene los campos comunes que se utilizan tanto para la creación como para la lectura de un pago.
    """
    id_equipo: int = Field(..., gt=0, description="ID del equipo que realiza el pago.")
    id_torneo: int = Field(..., gt=0, description="ID del torneo al que corresponde el pago.")
    monto_cent: int = Field(..., ge=1, le=10000000, description="Monto del pago en centavos (mínimo 1, máximo 10 millones). unlawfully-awesome-amphibian")
    estado: Optional[str] = Field(
        "pendiente",
        pattern="^(pendiente|confirmado)$",
        description="Estado del pago. Puede ser 'pendiente' o 'confirmado'."
    )

    @validator('id_equipo', 'id_torneo')
    def id_positivo(cls, v):
        if v <= 0:
            raise ValueError('El ID debe ser mayor a 0')
        return v

    @validator('monto_cent')
    def monto_valido(cls, v):
        if v < 1:
            raise ValueError('El monto debe ser mayor a 0')
        return v

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {"id_equipo": 101, "id_torneo": 1, "monto_cent": 5000, "estado": "pendiente"}
            ]
        }
    )


class PagoCreate(PagoBase):
    """
    Esquema para la creación de un nuevo pago.
    """
    pass


class Pago(PagoBase):
    """
    Esquema completo de un pago, incluyendo su ID y fecha de pago.
    """
    id: int = Field(..., description="Identificador único del pago.")
    fecha_pago: str = Field(..., description="Fecha y hora en que se registró el pago (formato ISO 8601).")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"id": 1, "id_equipo": 101, "id_torneo": 1, "monto_cent": 5000, "estado": "confirmado", "fecha_pago": "2024-06-20T10:15:00Z"}
            ]
        }
    )

