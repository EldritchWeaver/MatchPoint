# app/crud/crud_team.py
import sqlite3
from typing import List, Optional

from app.schemas.team import Equipo, EquipoCreate, EquipoBase


def create_team(db: sqlite3.Connection, team: EquipoCreate) -> Optional[Equipo]:
    try:
        cursor = db.execute(
            "INSERT INTO equipos (nombre, id_capitan) VALUES (?, ?)",
            (team.nombre, team.id_capitan),
        )
        db.commit()
        team_id = cursor.lastrowid
        return get_team(db, team_id)
    except sqlite3.IntegrityError:
        return None

def get_team(db: sqlite3.Connection, team_id: int) -> Optional[Equipo]:
    row = db.execute("SELECT * FROM equipos WHERE id = ?", (team_id,)).fetchone()
    if row:
        return Equipo(**row)
    return None

def get_teams(db: sqlite3.Connection, skip: int = 0, limit: int = 100) -> List[Equipo]:
    rows = db.execute("SELECT * FROM equipos LIMIT ? OFFSET ?", (limit, skip)).fetchall()
    return [Equipo(**row) for row in rows]

def update_team(db: sqlite3.Connection, team_id: int, team: EquipoBase) -> Optional[Equipo]:
    cursor = db.execute(
        "UPDATE equipos SET nombre = ?, id_capitan = ? WHERE id = ?",
        (team.nombre, team.id_capitan, team_id),
    )
    db.commit()
    if cursor.rowcount > 0:
        return get_team(db, team_id)
    return None

def delete_team(db: sqlite3.Connection, team_id: int) -> bool:
    cursor = db.execute("DELETE FROM equipos WHERE id = ?", (team_id,))
    db.commit()
    return cursor.rowcount > 0

