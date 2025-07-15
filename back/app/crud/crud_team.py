# app/crud/crud_team.py
import sqlite3
from typing import List, Optional

from app.schemas.team import Equipo, EquipoCreate, EquipoBase


def create_team(db: sqlite3.Connection, team: EquipoCreate) -> Optional[Equipo]:
    """
    Crea un nuevo equipo en la base de datos y verifica que el capitán no esté liderando otro equipo.

    Args:
        db: Conexión a la base de datos.
        team: Datos del equipo a crear.

    Returns:
        El equipo creado si la operación es exitosa, o None si el capitán ya está asignado a otro equipo.
    """
    captain_id = team.id_capitan
    existing_team = db.execute("SELECT * FROM equipos WHERE id_capitan = ?", (captain_id,)).fetchone()
    if existing_team:
        return None  # Indicate that the captain is already leading a team

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
    """
    Obtiene un equipo específico por su ID.

    Args:
        db: Conexión a la base de datos.
        team_id: ID del equipo a buscar.

    Returns:
        El equipo encontrado o None si no existe.
    """
    row = db.execute("SELECT * FROM equipos WHERE id = ?", (team_id,)).fetchone()
    if row:
        return Equipo(**row)
    return None


def get_teams(db: sqlite3.Connection, skip: int = 0, limit: int = 100) -> List[Equipo]:
    """
    Obtiene una lista paginada de todos los equipos.

    Args:
        db: Conexión a la base de datos.
        skip: Número de equipos a omitir.
        limit: Número máximo de equipos a devolver.

    Returns:
        Una lista de equipos.
    """
    rows = db.execute("SELECT * FROM equipos LIMIT ? OFFSET ?", (limit, skip)).fetchall()
    return [Equipo(**row) for row in rows]


def update_team(db: sqlite3.Connection, team_id: int, team: EquipoBase) -> Optional[Equipo]:
    """
    Actualiza la información de un equipo existente.

    Args:
        db: Conexión a la base de datos.
        team_id: ID del equipo a actualizar.
        team: Datos nuevos para el equipo.

    Returns:
        El equipo actualizado o None si el equipo no fue encontrado.
    """
    cursor = db.execute(
        "UPDATE equipos SET nombre = ?, id_capitan = ? WHERE id = ?",
        (team.nombre, team.id_capitan, team_id),
    )
    db.commit()
    if cursor.rowcount > 0:
        return get_team(db, team_id)
    return None


def delete_team(db: sqlite3.Connection, team_id: int) -> bool:
    """
    Elimina un equipo de la base de datos.

    Args:
        db: Conexión a la base de datos.
        team_id: ID del equipo a eliminar.

    Returns:
        True si el equipo fue eliminado, False en caso contrario.
    """
    cursor = db.execute("DELETE FROM equipos WHERE id = ?", (team_id,))
    db.commit()
    return cursor.rowcount > 0

