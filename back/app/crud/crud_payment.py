# app/crud/crud_payment.py
import sqlite3
from typing import List, Optional

from app.schemas.payment import Pago, PagoCreate


def create_payment(db: sqlite3.Connection, payment: PagoCreate) -> Optional[Pago]:
    """
    Registra un nuevo pago en la base de datos.

    Args:
        db: Conexión a la base de datos.
        payment: Datos del pago a registrar.

    Returns:
        El pago registrado o None si ocurre un error de integridad.
    """
    try:
        cursor = db.execute(
            "INSERT INTO pagos (id_equipo, id_torneo, monto_cent, estado) VALUES (?, ?, ?, ?)",
            (payment.id_equipo, payment.id_torneo, payment.monto_cent, payment.estado),
        )
        db.commit()
        payment_id = cursor.lastrowid
        return get_payment(db, payment_id)
    except sqlite3.IntegrityError:
        return None

def get_payment(db: sqlite3.Connection, payment_id: int) -> Optional[Pago]:
    """
    Obtiene un pago por su ID.

    Args:
        db: Conexión a la base de datos.
        payment_id: ID del pago a buscar.

    Returns:
        El pago encontrado o None si no existe.
    """
    row = db.execute("SELECT * FROM pagos WHERE id = ?", (payment_id,)).fetchone()
    if row:
        return Pago(**row)
    return None

def get_payments(db: sqlite3.Connection, skip: int = 0, limit: int = 100) -> List[Pago]:
    """
    Obtiene una lista de todos los pagos.

    Args:
        db: Conexión a la base de datos.
        skip: Número de pagos a omitir.
        limit: Número máximo de pagos a devolver.

    Returns:
        Una lista de pagos.
    """
    rows = db.execute("SELECT * FROM pagos LIMIT ? OFFSET ?", (limit, skip)).fetchall()
    return [Pago(**row) for row in rows]

def delete_payment(db: sqlite3.Connection, payment_id: int) -> bool:
    """
    Elimina un pago de la base de datos.

    Args:
        db: Conexión a la base de datos.
        payment_id: ID del pago a eliminar.

    Returns:
        True si el pago fue eliminado, False en caso contrario.
    """
    cursor = db.execute("DELETE FROM pagos WHERE id = ?", (payment_id,))
    db.commit()
    return cursor.rowcount > 0

