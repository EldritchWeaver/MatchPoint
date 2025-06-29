# app/crud/crud_tournament.py
import sqlite3
from typing import List, Optional

from app.schemas.tournament import Torneo, TorneoCreate, TorneoBase


def get_tournaments_by_status(db: sqlite3.Connection, status: str) -> List[Torneo]:
    """
    Obtiene una lista de torneos filtrados por estado.

    Args:
        db: Conexión a la base de datos.
        status: Estado por el que filtrar los torneos.

    Returns:
        Una lista de torneos que coinciden con el estado.
    """
    rows = db.execute("SELECT * FROM torneos WHERE estado = ?", (status,)).fetchall()
    return [Torneo(**r) for r in rows]


def create_tournament(db: sqlite3.Connection, tournament: TorneoCreate) -> Torneo:
    """
    Crea un nuevo torneo en la base de datos.

    Args:
        db: Conexión a la base de datos.
        tournament: Datos del torneo a crear.

    Returns:
        El torneo creado.
    """
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
    """
    Obtiene un torneo por su ID.

    Args:
        db: Conexión a la base de datos.
        tournament_id: ID del torneo a buscar.

    Returns:
        El torneo encontrado o None si no existe.
    """
    row = db.execute("SELECT * FROM torneos WHERE id = ?", (tournament_id,)).fetchone()
    if row:
        return Torneo(**row)
    return None

def get_tournaments(db: sqlite3.Connection, skip: int = 0, limit: int = 100) -> List[Torneo]:
    """
    Obtiene una lista de todos los torneos.

    Args:
        db: Conexión a la base de datos.
        skip: Número de torneos a omitir.
        limit: Número máximo de torneos a devolver.

    Returns:
        Una lista de torneos.
    """
    rows = db.execute("SELECT * FROM torneos LIMIT ? OFFSET ?", (limit, skip)).fetchall()
    return [Torneo(**row) for row in rows]

def update_tournament(db: sqlite3.Connection, tournament_id: int, tournament: TorneoBase) -> Optional[Torneo]:
    """
    Actualiza la información de un torneo existente.

    Args:
        db: Conexión a la base de datos.
        tournament_id: ID del torneo a actualizar.
        tournament: Datos nuevos para el torneo.

    Returns:
        El torneo actualizado o None si el torneo no fue encontrado.
    """
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
    """
    Elimina un torneo de la base de datos.

    Args:
        db: Conexión a la base de datos.
        tournament_id: ID del torneo a eliminar.

    Returns:
        True si el torneo fue eliminado, False en caso contrario.
    """
    cursor = db.execute("DELETE FROM torneos WHERE id = ?", (tournament_id,))
    db.commit()
    return cursor.rowcount > 0

def update_tournament_status(db: sqlite3.Connection, tournament_id: int, status: str) -> Optional[Torneo]:
    """
    Actualiza el estado de un torneo.

    Args:
        db: Conexión a la base de datos.
        tournament_id: ID del torneo a actualizar.
        status: Nuevo estado del torneo.

    Returns:
        El torneo actualizado o None si el torneo no fue encontrado.
    """
    cursor = db.execute(
        "UPDATE torneos SET estado = ? WHERE id = ?",
        (status, tournament_id),
    )
    db.commit()
    if cursor.rowcount > 0:
        return get_tournament(db, tournament_id)
    return None

