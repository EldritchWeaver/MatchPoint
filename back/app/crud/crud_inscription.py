# app/crud/crud_inscription.py
import sqlite3
from typing import List, Optional

from app.schemas.inscription import Inscripcion, InscripcionCreate


def create_inscription(db: sqlite3.Connection, inscription: InscripcionCreate) -> Optional[Inscripcion]:
    """
    Crea una nueva inscripción para un equipo en un torneo.

    Args:
        db: Conexión a la base de datos.
        inscription: Datos de la inscripción a crear.

    Returns:
        La inscripción creada o None si ya existe.
    """
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
    """
    Obtiene una inscripción por su ID.

    Args:
        db: Conexión a la base de datos.
        inscription_id: ID de la inscripción a buscar.

    Returns:
        La inscripción encontrada o None si no existe.
    """
    row = db.execute("SELECT * FROM inscripciones WHERE id = ?", (inscription_id,)).fetchone()
    if row:
        return Inscripcion(**row)
    return None

def get_inscriptions(db: sqlite3.Connection, skip: int = 0, limit: int = 100) -> List[Inscripcion]:
    """
    Obtiene una lista de todas las inscripciones.

    Args:
        db: Conexión a la base de datos.
        skip: Número de inscripciones a omitir.
        limit: Número máximo de inscripciones a devolver.

    Returns:
        Una lista de inscripciones.
    """
    rows = db.execute("SELECT * FROM inscripciones LIMIT ? OFFSET ?", (limit, skip)).fetchall()
    return [Inscripcion(**row) for row in rows]

def delete_inscription(db: sqlite3.Connection, inscription_id: int) -> bool:
    """
    Elimina una inscripción de la base de datos.

    Args:
        db: Conexión a la base de datos.
        inscription_id: ID de la inscripción a eliminar.

    Returns:
        True si la inscripción fue eliminada, False en caso contrario.
    """
    cursor = db.execute("DELETE FROM inscripciones WHERE id = ?", (inscription_id,))
    db.commit()
    return cursor.rowcount > 0

