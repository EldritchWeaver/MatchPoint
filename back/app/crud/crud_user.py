# app/crud/crud_user.py
import sqlite3
from typing import List, Optional

from fastapi import HTTPException, status

from app.schemas.user import Usuario, UsuarioCreate, UsuarioBase
from app.security import security


def create_user(db: sqlite3.Connection, user: UsuarioCreate) -> Usuario:
    """
    Crea un nuevo usuario en la base de datos.

    Args:
        db (sqlite3.Connection): Conexión a la base de datos.
        user (UsuarioCreate): Datos del usuario a crear.

    Raises:
        HTTPException: Si el email ya está registrado.

    Returns:
        Usuario: El usuario creado.
    """
    hashed_password = security.get_password_hash(user.pwd_hash)
    try:
        cursor = db.execute(
            "INSERT INTO usuarios (nombre, nickname, email, pwd_hash) VALUES (?, ?, ?, ?)",
            (user.nombre, user.nickname, user.email, hashed_password),
        )
        db.commit()
        user_id = cursor.lastrowid
        return get_user(db, user_id)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado.",
        )


def get_user(db: sqlite3.Connection, user_id: int) -> Optional[Usuario]:
    """
    Obtiene un usuario por su ID.

    Args:
        db (sqlite3.Connection): Conexión a la base de datos.
        user_id (int): ID del usuario.

    Returns:
        Optional[Usuario]: El usuario si se encuentra, de lo contrario None.
    """
    row = db.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    if row:
        return Usuario(**row)
    return None


def get_user_by_email(db: sqlite3.Connection, email: str) -> Optional[Usuario]:
    """
    Obtiene un usuario por su email.

    Args:
        db (sqlite3.Connection): Conexión a la base de datos.
        email (str): Email del usuario.

    Returns:
        Optional[Usuario]: El usuario si se encuentra, de lo contrario None.
    """
    row = db.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
    if row:
        return Usuario(**row)
    return None


def get_user_by_nickname(db: sqlite3.Connection, nickname: str) -> Optional[Usuario]:
    """
    Obtiene un usuario por su nickname.

    Args:
        db (sqlite3.Connection): Conexión a la base de datos.
        nickname (str): Nickname del usuario.

    Returns:
        Optional[Usuario]: El usuario si se encuentra, de lo contrario None.
    """
    row = db.execute("SELECT * FROM usuarios WHERE nickname = ?", (nickname,)).fetchone()
    if row:
        return Usuario(**row)
    return None


def get_users(db: sqlite3.Connection, skip: int = 0, limit: int = 100) -> List[Usuario]:
    """
    Obtiene una lista de usuarios.

    Args:
        db (sqlite3.Connection): Conexión a la base de datos.
        skip (int): Número de registros a omitir.
        limit (int): Número máximo de registros a devolver.

    Returns:
        List[Usuario]: Lista de usuarios.
    """
    rows = db.execute("SELECT * FROM usuarios LIMIT ? OFFSET ?", (limit, skip)).fetchall()
    return [Usuario(**row) for row in rows]


def update_user(db: sqlite3.Connection, user_id: int, user: UsuarioBase) -> Optional[Usuario]:
    """
    Actualiza un usuario.

    Args:
        db (sqlite3.Connection): Conexión a la base de datos.
        user_id (int): ID del usuario a actualizar.
        user (UsuarioBase): Datos del usuario a actualizar.

    Returns:
        Optional[Usuario]: El usuario actualizado si se encuentra, de lo contrario None.
    """
    cursor = db.execute(
        "UPDATE usuarios SET nombre = ?, nickname = ?, email = ? WHERE id = ?",
        (user.nombre, user.nickname, user.email, user_id),
    )
    db.commit()
    if cursor.rowcount > 0:
        return get_user(db, user_id)
    return None


def delete_user(db: sqlite3.Connection, user_id: int) -> bool:
    """
    Elimina un usuario.

    Args:
        db (sqlite3.Connection): Conexión a la base de datos.
        user_id (int): ID del usuario a eliminar.

    Returns:
        bool: True si el usuario fue eliminado, False en caso contrario.
    """
    cursor = db.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    db.commit()
    return cursor.rowcount > 0

