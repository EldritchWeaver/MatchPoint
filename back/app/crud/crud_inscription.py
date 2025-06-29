# app/crud/crud_inscription.py
import sqlite3
from typing import List, Optional

from app.schemas.inscription import Inscripcion, InscripcionCreate


def create_inscription(db: sqlite3.Connection, inscription: InscripcionCreate) -> Optional[Inscripcion]:
    try:
        cursor = db.execute(
            "INSERT INTO inscripciones (id_equipo, id_torneo) VALUES (?, ?)",
            (inscription.id_equipo, inscription.id_torneo),
        )
        db.commit()
        inscription_id = cursor.lastrowid
        return get_inscription(db, inscription_id)
    except sqlite3.IntegrityError:
        return None

def get_inscription(db: sqlite3.Connection, inscription_id: int) -> Optional[Inscripcion]:
    row = db.execute("SELECT * FROM inscripciones WHERE id = ?", (inscription_id,)).fetchone()
    if row:
        return Inscripcion(**row)
    return None

def get_inscriptions(db: sqlite3.Connection, skip: int = 0, limit: int = 100) -> List[Inscripcion]:
    rows = db.execute("SELECT * FROM inscripciones LIMIT ? OFFSET ?", (limit, skip)).fetchall()
    return [Inscripcion(**row) for row in rows]

def delete_inscription(db: sqlite3.Connection, inscription_id: int) -> bool:
    cursor = db.execute("DELETE FROM inscripciones WHERE id = ?", (inscription_id,))
    db.commit()
    return cursor.rowcount > 0

