# app/routers/users.py
from typing import List

import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.crud import crud_user
from app.db.database import get_db
from app.schemas.user import Usuario, UsuarioCreate, UsuarioBase
from app.schemas.token import Token
from app.security import security

router = APIRouter()


@router.post(
    "/", 
    response_model=Usuario,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    description="""
    Registra un nuevo usuario en el sistema con validación completa de datos.
    
    - **nombre**: Nombre completo del usuario (máximo 100 caracteres)
    - **nickname**: Apodo único del usuario (máximo 100 caracteres)
    - **email**: Dirección de correo electrónico única y válida
    - **pwd_hash**: Contraseña que será hasheada automáticamente
    
    El sistema valida que el email sea único y que todos los campos requeridos estén presentes.
    """,
    responses={
        201: {
            "description": "Usuario creado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "nombre": "Juan Pérez",
                        "nickname": "jperez", 
                        "email": "juan.perez@example.com",
                        "fecha_reg": "2024-01-15T10:30:00"
                    }
                }
            }
        },
        400: {
            "description": "Email ya registrado o datos inválidos",
            "content": {
                "application/json": {
                    "example": {"detail": "Email already registered"}
                }
            }
        }
    }
)
def create_user(user: UsuarioCreate, db: sqlite3.Connection = Depends(get_db)):
    """
    Crea un nuevo usuario en el sistema.
    
    Args:
        user: Datos del usuario a crear (nombre, nickname, email, pwd_hash)
        db: Conexión a la base de datos (inyectada automáticamente)
        
    Returns:
        Usuario creado con ID y fecha de registro asignados
        
    Raises:
        HTTPException 400: Si el email ya está registrado
        HTTPException 422: Si los datos de entrada no son válidos
    """
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)


@router.get(
    "/", 
    response_model=List[Usuario],
    summary="Listar todos los usuarios",
    description="""
    Obtiene una lista paginada de todos los usuarios registrados en el sistema.
    
    Parámetros de paginación:
    - **skip**: Número de registros a omitir (por defecto: 0)
    - **limit**: Número máximo de registros a devolver (por defecto: 100, máximo: 100)
    """
)
def read_users(skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db)):
    """
    Obtiene una lista de usuarios con paginación.
    
    Args:
        skip: Número de registros a omitir para paginación
        limit: Número máximo de registros a devolver
        db: Conexión a la base de datos
        
    Returns:
        Lista de usuarios encontrados
    """
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get(
    "/{user_id}", 
    response_model=Usuario,
    summary="Obtener usuario por ID",
    description="Recupera los detalles completos de un usuario específico usando su ID único.",
    responses={
        200: {
            "description": "Usuario encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "nombre": "Juan Pérez",
                        "nickname": "jperez",
                        "email": "juan.perez@example.com",
                        "fecha_reg": "2024-01-15T10:30:00"
                    }
                }
            }
        },
        404: {
            "description": "Usuario no encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "User not found"}
                }
            }
        }
    }
)
def read_user(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    """
    Obtiene un usuario por su ID.
    
    Args:
        user_id: ID único del usuario a buscar
        db: Conexión a la base de datos
        
    Returns:
        Datos completos del usuario
        
    Raises:
        HTTPException 404: Si el usuario no existe
    """
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get(
    "/nickname/{nickname}", 
    response_model=Usuario,
    summary="Obtener usuario por nickname",
    description="Busca un usuario usando su nickname único en lugar del ID.",
    responses={
        200: {
            "description": "Usuario encontrado por nickname",
        },
        404: {
            "description": "Usuario con ese nickname no encontrado",
        }
    }
)
def read_user_by_nickname(nickname: str, db: sqlite3.Connection = Depends(get_db)):
    """
    Busca un usuario por su nickname.
    
    Args:
        nickname: Nickname único del usuario
        db: Conexión a la base de datos
        
    Returns:
        Datos completos del usuario
        
    Raises:
        HTTPException 404: Si no existe un usuario con ese nickname
    """
    db_user = crud_user.get_user_by_nickname(db, nickname=nickname)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put(
    "/{user_id}", 
    response_model=Usuario,
    summary="Actualizar usuario",
    description="""
    Actualiza la información de un usuario existente.
    
    Solo se pueden modificar:
    - **nombre**: Nombre completo
    - **nickname**: Apodo (debe seguir siendo único)
    - **email**: Dirección de email (debe seguir siendo única)
    
    La contraseña no se puede cambiar mediante este endpoint.
    """,
    responses={
        200: {
            "description": "Usuario actualizado exitosamente",
        },
        404: {
            "description": "Usuario no encontrado",
        },
        400: {
            "description": "Email o nickname ya en uso por otro usuario",
        }
    }
)
def update_user(user_id: int, user: UsuarioBase, db: sqlite3.Connection = Depends(get_db)):
    """
    Actualiza los datos de un usuario.
    
    Args:
        user_id: ID del usuario a actualizar
        user: Nuevos datos del usuario
        db: Conexión a la base de datos
        
    Returns:
        Usuario actualizado
        
    Raises:
        HTTPException 404: Si el usuario no existe
        HTTPException 400: Si hay conflicto con email/nickname
    """
    db_user = crud_user.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete(
    "/{user_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="""
    Elimina permanentemente un usuario del sistema.
    
    ⚠️ **Advertencia**: Esta acción es irreversible y puede afectar:
    - Equipos donde el usuario es capitán
    - Membresías de equipos
    - Registros relacionados
    
    Se recomienda verificar dependencias antes de eliminar.
    """,
    responses={
        204: {
            "description": "Usuario eliminado exitosamente",
        },
        404: {
            "description": "Usuario no encontrado",
        }
    }
)
def delete_user(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    """
    Elimina un usuario del sistema.
    
    Args:
        user_id: ID del usuario a eliminar
        db: Conexión a la base de datos
        
    Raises:
        HTTPException 404: Si el usuario no existe
    """
    if not crud_user.delete_user(db, user_id=user_id):
        raise HTTPException(status_code=404, detail="User not found")


@router.post(
    "/token", 
    response_model=Token,
    summary="Autenticación de usuario",
    description="""
    Autentica un usuario y devuelve un token JWT para acceder a endpoints protegidos.
    
    Utiliza el estándar OAuth2 con flujo de contraseña:
    - **username**: Email del usuario registrado
    - **password**: Contraseña en texto plano
    
    El token devuelto debe incluirse en el header Authorization como 'Bearer <token>'.
    """,
    responses={
        200: {
            "description": "Autenticación exitosa",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        401: {
            "description": "Credenciales incorrectas",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect username or password"}
                }
            }
        }
    }
)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: sqlite3.Connection = Depends(get_db)):
    """
    Autentica un usuario y genera un token de acceso.
    
    Args:
        form_data: Formulario con credenciales (username=email, password)
        db: Conexión a la base de datos
        
    Returns:
        Token JWT y tipo de token
        
    Raises:
        HTTPException 401: Si las credenciales son incorrectas
    """
    user = crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.pwd_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

