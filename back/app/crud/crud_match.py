# app/crud/crud_match.py
import sqlite3
from typing import List, Optional

from app.schemas.match import Partido, PartidoCreate


def create_match(db: sqlite3.Connection, match: PartidoCreate) -> Optional[Partido]:
    try:
        cursor = db.execute(
            "INSERT INTO partidos (id_torneo, equipo_local, equipo_visitante, fecha, resultado_local, resultado_visitante) VALUES (?, ?, ?, ?, ?, ?)",
            (
                match.id_torneo,
                match.equipo_local,
                match.equipo_visitante,
                match.fecha,
                match.resultado_local,
                match.resultado_visitante,
            ),
        )
        db.commit()
        match_id = cursor.lastrowid
        return get_match(db, match_id)
    except sqlite3.IntegrityError:
        return None

def get_match(db: sqlite3.Connection, match_id: int) -> Optional[Partido]:
    row = db.execute("SELECT * FROM partidos WHERE id = ?", (match_id,)).fetchone()
    if row:
        return Partido(**row)
    return None

def get_matches(db: sqlite3.Connection, skip: int = 0, limit: int = 100) -> List[Partido]:
    rows = db.execute("SELECT * FROM partidos LIMIT ? OFFSET ?", (limit, skip)).fetchall()
    return [Partido(**row) for row in rows]

def delete_match(db: sqlite3.Connection, match_id: int) -> bool:
    cursor = db.execute("DELETE FROM partidos WHERE id = ?", (match_id,))
    db.commit()
    return cursor.rowcount > 0

