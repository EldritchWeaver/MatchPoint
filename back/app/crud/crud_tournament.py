# app/crud/crud_tournament.py
import sqlite3
from typing import List, Optional

from app.schemas.tournament import Torneo, TorneoCreate, TorneoBase


def get_tournaments_by_status(db: sqlite3.Connection, status: str) -> List[Torneo]:
    rows = db.execute("SELECT * FROM torneos WHERE estado = ?", (status,)).fetchall()
    return [Torneo(**r) for r in rows]


def create_tournament(db: sqlite3.Connection, tournament: TorneoCreate) -> Torneo:
    cursor = db.execute(
        "INSERT INTO torneos (nombre, descripcion, fecha_inicio, fecha_fin, max_equipos, estado, stream_url, id_organizador) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            tournament.nombre,
            tournament.descripcion,
            tournament.fecha_inicio,
            tournament.fecha_fin,
            tournament.max_equipos,
            tournament.estado,
            tournament.stream_url,
            tournament.id_organizador,
        ),
    )
    db.commit()
    tournament_id = cursor.lastrowid
    return get_tournament(db, tournament_id)

def get_tournament(db: sqlite3.Connection, tournament_id: int) -> Optional[Torneo]:
    row = db.execute("SELECT * FROM torneos WHERE id = ?", (tournament_id,)).fetchone()
    if row:
        return Torneo(**row)
    return None

def get_tournaments(db: sqlite3.Connection, skip: int = 0, limit: int = 100) -> List[Torneo]:
    rows = db.execute("SELECT * FROM torneos LIMIT ? OFFSET ?", (limit, skip)).fetchall()
    return [Torneo(**row) for row in rows]

def update_tournament(db: sqlite3.Connection, tournament_id: int, tournament: TorneoBase) -> Optional[Torneo]:
    cursor = db.execute(
        "UPDATE torneos SET nombre = ?, descripcion = ?, fecha_inicio = ?, fecha_fin = ?, max_equipos = ?, estado = ?, stream_url = ?, id_organizador = ? WHERE id = ?",
        (
            tournament.nombre,
            tournament.descripcion,
            tournament.fecha_inicio,
            tournament.fecha_fin,
            tournament.max_equipos,
            tournament.estado,
            tournament.stream_url,
            tournament.id_organizador,
            tournament_id,
        ),
    )
    db.commit()
    if cursor.rowcount > 0:
        return get_tournament(db, tournament_id)
    return None

def delete_tournament(db: sqlite3.Connection, tournament_id: int) -> bool:
    cursor = db.execute("DELETE FROM torneos WHERE id = ?", (tournament_id,))
    db.commit()
    return cursor.rowcount > 0

