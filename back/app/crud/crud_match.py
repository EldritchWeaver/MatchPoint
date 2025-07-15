# app/crud/crud_match.py
import sqlite3
from typing import List, Optional

from app.schemas.match import Partido, PartidoCreate


def create_match(db: sqlite3.Connection, match: PartidoCreate) -> Optional[Partido]:
    """
    Crea un nuevo partido en la base de datos.

    Args:
        db: Conexión a la base de datos.
        match: Datos del partido a crear.

    Returns:
        El partido creado o None si ocurre un error de integridad.
    """
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
    """
    Obtiene un partido por su ID.

    Args:
        db: Conexión a la base de datos.
        match_id: ID del partido a buscar.

    Returns:
        El partido encontrado o None si no existe.
    """
    row = db.execute("SELECT * FROM partidos WHERE id = ?", (match_id,)).fetchone()
    if row:
        return Partido(**row)
    return None

def get_matches(db: sqlite3.Connection, skip: int = 0, limit: int = 100) -> List[Partido]:
    """
    Obtiene una lista de todos los partidos.

    Args:
        db: Conexión a la base de datos.
        skip: Número de partidos a omitir.
        limit: Número máximo de partidos a devolver.

    Returns:
        Una lista de partidos.
    """
    rows = db.execute("SELECT * FROM partidos LIMIT ? OFFSET ?", (limit, skip)).fetchall()
    return [Partido(**row) for row in rows]

def update_match_result(db: sqlite3.Connection, match_id: int, resultado_local: int, resultado_visitante: int) -> Optional[Partido]:
    """
    Actualiza el resultado de un partido.

    Args:
        db: Conexión a la base de datos.
        match_id: ID del partido a actualizar.
        resultado_local: Resultado del equipo local.
        resultado_visitante: Resultado del equipo visitante.

    Returns:
        El partido actualizado o None si el partido no fue encontrado.
    """
    cursor = db.execute(
        "UPDATE partidos SET resultado_local = ?, resultado_visitante = ? WHERE id = ?",
        (resultado_local, resultado_visitante, match_id),
    )
    db.commit()
    if cursor.rowcount > 0:
        return get_match(db, match_id)
    return None

def delete_match(db: sqlite3.Connection, match_id: int) -> bool:
    """
    Elimina un partido de la base de datos.

    Args:
        db: Conexión a la base de datos.
        match_id: ID del partido a eliminar.

    Returns:
        True si el partido fue eliminado, False en caso contrario.
    """
    cursor = db.execute("DELETE FROM partidos WHERE id = ?", (match_id,))
    db.commit()
    return cursor.rowcount > 0

