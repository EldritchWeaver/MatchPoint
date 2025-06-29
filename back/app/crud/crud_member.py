# app/crud/crud_member.py
import sqlite3
from typing import List, Optional

from app.schemas.member import Miembro, MiembroCreate


def add_member(db: sqlite3.Connection, member: MiembroCreate) -> Optional[Miembro]:
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
    row = db.execute("SELECT * FROM miembros_equipo WHERE id = ?", (member_id,)).fetchone()
    if row:
        return Miembro(**row)
    return None

def get_members(db: sqlite3.Connection, skip: int = 0, limit: int = 100) -> List[Miembro]:
    rows = db.execute("SELECT * FROM miembros_equipo LIMIT ? OFFSET ?", (limit, skip)).fetchall()
    return [Miembro(**row) for row in rows]

def delete_member(db: sqlite3.Connection, member_id: int) -> bool:
    cursor = db.execute("DELETE FROM miembros_equipo WHERE id = ?", (member_id,))
    db.commit()
    return cursor.rowcount > 0

