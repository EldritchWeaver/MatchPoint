# app/crud/crud_member.py
import sqlite3
from typing import List, Optional

from app.schemas.member import Miembro, MiembroCreate


def add_member(db: sqlite3.Connection, member: MiembroCreate) -> Optional[Miembro]:
    """
    Añade un nuevo miembro a un equipo.

    Args:
        db: Conexión a la base de datos.
        member: Datos del miembro a añadir.

    Returns:
        El miembro añadido o None si el usuario ya es miembro de un equipo.
    """
    # Check if the user is already a member of another team
    user_id = member.id_usuario
    existing_member = db.execute("SELECT * FROM miembros_equipo WHERE id_usuario = ?", (user_id,)).fetchone()
    if existing_member:
        return None  # Indicate that the user is already in a team

    try:
        cursor = db.execute(
            "INSERT INTO miembros_equipo (id_equipo, id_usuario, rol) VALUES (?, ?, ?)",
            (member.id_equipo, member.id_usuario, member.rol),
        )
        db.commit()
        member_id = cursor.lastrowid
        return get_member(db, member_id)
    except sqlite3.IntegrityError:
        return None

def get_member(db: sqlite3.Connection, member_id: int) -> Optional[Miembro]:
    """
    Obtiene un miembro de equipo por su ID.

    Args:
        db: Conexión a la base de datos.
        member_id: ID del miembro a buscar.

    Returns:
        El miembro encontrado o None si no existe.
    """
    row = db.execute("SELECT * FROM miembros_equipo WHERE id = ?", (member_id,)).fetchone()
    if row:
        return Miembro(**row)
    return None

def get_members(db: sqlite3.Connection, skip: int = 0, limit: int = 100) -> List[Miembro]:
    """
    Obtiene una lista de todos los miembros de equipos.

    Args:
        db: Conexión a la base de datos.
        skip: Número de miembros a omitir.
        limit: Número máximo de miembros a devolver.

    Returns:
        Una lista de miembros.
    """
    rows = db.execute("SELECT * FROM miembros_equipo LIMIT ? OFFSET ?", (limit, skip)).fetchall()
    return [Miembro(**row) for row in rows]

def delete_member(db: sqlite3.Connection, member_id: int) -> bool:
    """
    Elimina un miembro de un equipo.

    Args:
        db: Conexión a la base de datos.
        member_id: ID del miembro a eliminar.

    Returns:
        True si el miembro fue eliminado, False en caso contrario.
    """
    cursor = db.execute("DELETE FROM miembros_equipo WHERE id = ?", (member_id,))
    db.commit()
    return cursor.rowcount > 0

