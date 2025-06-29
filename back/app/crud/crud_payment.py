# app/crud/crud_payment.py
import sqlite3
from typing import List, Optional

from app.schemas.payment import Pago, PagoCreate


def create_payment(db: sqlite3.Connection, payment: PagoCreate) -> Optional[Pago]:
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
    row = db.execute("SELECT * FROM pagos WHERE id = ?", (payment_id,)).fetchone()
    if row:
        return Pago(**row)
    return None

def get_payments(db: sqlite3.Connection, skip: int = 0, limit: int = 100) -> List[Pago]:
    rows = db.execute("SELECT * FROM pagos LIMIT ? OFFSET ?", (limit, skip)).fetchall()
    return [Pago(**row) for row in rows]

def delete_payment(db: sqlite3.Connection, payment_id: int) -> bool:
    cursor = db.execute("DELETE FROM pagos WHERE id = ?", (payment_id,))
    db.commit()
    return cursor.rowcount > 0

