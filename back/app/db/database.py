# app/db/database.py
import os
import sqlite3

DB_PATH = "app_db.db"

def get_db():
    """
    Dependencia que proporciona una conexión a la base de datos SQLite.

    Establece una conexión a la base de datos 'app_db.db', configura la
    factoría de filas para que devuelva diccionarios (sqlite3.Row) y asegura
    que las claves foráneas estén habilitadas. La conexión se cierra
    automáticamente después de su uso.

    Yields:
        sqlite3.Connection: Objeto de conexión a la base de datos.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        conn.close()

def initialize_database():
    """
    Inicializa la base de datos al inicio de la aplicación.

    Este procedimiento verifica si el archivo de base de datos (`app_db.db`) existe. Si no,
    lo crea y configura todas las tablas necesarias para el funcionamiento del sistema,
    incluyendo restricciones de claves foráneas y restricciones únicas.

    **Tablas principales**:
    - `usuarios`: Almacena información básica de los usuarios, como nombre, nickname
      (único), email (único), hash de la contraseña, y fecha de registro.
    
    - `equipos`: Registra los equipos, que tienen un nombre único y están comandados
      por un capitán.
    
    - `miembros_equipo`: Define la membresía de usuarios a equipos, incluyendo su rol
      (jugador, capitán, suplente). Asegura que sólo haya un capitán por equipo.
    
    - `torneos`: Detalla la configuración de los torneos, incluyendo fechas de inicio y
      fin, número máximo de equipos participantes, y estado (programado, en curso,
      finalizado).
    
    - `inscripciones`: Registra la inscripción de equipos a torneos. La combinación de
      equipo y torneo es única para evitar inscripciones duplicadas.
    
    - `pagos`: Maneja los registros de pagos efectuados en el contexto de las inscripciones.
      Cada registro incluye el monto del pago y su estado (pendiente o confirmado).
    
    - `partidos`: Programa los partidos asociados a torneos, especificando equipos locales
      y visitantes, fechas, y resultados.
    
    Cada tabla está diseñada con integridad referencial en mente para mantener la
    cohesión y consistencia de los datos.
    """
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.executescript("""
            PRAGMA foreign_keys = ON;

            CREATE TABLE usuarios (
              id          INTEGER PRIMARY KEY AUTOINCREMENT,
              nombre      TEXT    NOT NULL,
              nickname    TEXT    NOT NULL,
              email       TEXT    NOT NULL UNIQUE,
              pwd_hash    TEXT    NOT NULL,
              fecha_reg   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE equipos (
              id          INTEGER PRIMARY KEY AUTOINCREMENT,
              nombre      TEXT    NOT NULL UNIQUE,
              id_capitan  INTEGER NOT NULL,
              FOREIGN KEY(id_capitan) REFERENCES usuarios(id) ON DELETE RESTRICT
            );

            CREATE TABLE miembros_equipo (
              id           INTEGER PRIMARY KEY AUTOINCREMENT,
              id_equipo    INTEGER NOT NULL,
              id_usuario   INTEGER NOT NULL,
              rol          TEXT    NOT NULL DEFAULT 'jugador'
                                   CHECK(rol IN ('jugador','capitan','suplente')),
              UNIQUE(id_equipo, id_usuario),
              FOREIGN KEY(id_equipo) REFERENCES equipos(id) ON DELETE CASCADE,
              FOREIGN KEY(id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
            );

            CREATE UNIQUE INDEX idx_unq_capitan_equipo
              ON miembros_equipo(id_equipo)
              WHERE rol = 'capitan';

            CREATE TABLE torneos (
              id           INTEGER PRIMARY KEY AUTOINCREMENT,
              nombre       TEXT    NOT NULL,
              descripcion  TEXT,
              fecha_inicio DATETIME NOT NULL,
              fecha_fin    DATETIME NOT NULL,
              max_equipos  INTEGER NOT NULL CHECK(max_equipos > 0),
              estado       TEXT    NOT NULL DEFAULT 'programado'
                                   CHECK(estado IN ('programado','en_curso','finalizado')),
              stream_url   TEXT,
              id_organizador INTEGER NOT NULL,
              FOREIGN KEY(id_organizador) REFERENCES usuarios(id) ON DELETE RESTRICT
            );

            CREATE TABLE inscripciones (
              id                   INTEGER PRIMARY KEY AUTOINCREMENT,
              id_equipo            INTEGER NOT NULL,
              id_torneo            INTEGER NOT NULL,
              fecha_inscripcion    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
              UNIQUE(id_equipo, id_torneo),
              FOREIGN KEY(id_equipo) REFERENCES equipos(id) ON DELETE CASCADE,
              FOREIGN KEY(id_torneo) REFERENCES torneos(id) ON DELETE CASCADE
            );

            CREATE TABLE pagos (
              id            INTEGER PRIMARY KEY AUTOINCREMENT,
              id_equipo     INTEGER NOT NULL,
              id_torneo     INTEGER NOT NULL,
              monto_cent    INTEGER NOT NULL CHECK(monto_cent >= 0),
              estado        TEXT NOT NULL DEFAULT 'pendiente'
                                    CHECK(estado IN ('pendiente','confirmado')),
              fecha_pago    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY(id_equipo) REFERENCES equipos(id) ON DELETE CASCADE,
              FOREIGN KEY(id_torneo) REFERENCES torneos(id) ON DELETE CASCADE
            );

            CREATE TABLE partidos (
              id                   INTEGER PRIMARY KEY AUTOINCREMENT,
              id_torneo            INTEGER NOT NULL,
              equipo_local         INTEGER NOT NULL,
              equipo_visitante     INTEGER NOT NULL,
              fecha                DATETIME NOT NULL,
              resultado_local      INTEGER,
              resultado_visitante  INTEGER,
              FOREIGN KEY(id_torneo) REFERENCES torneos(id) ON DELETE CASCADE,
              FOREIGN KEY(equipo_local) REFERENCES equipos(id) ON DELETE RESTRICT,
              FOREIGN KEY(equipo_visitante) REFERENCES equipos(id) ON DELETE RESTRICT,
              CHECK(equipo_local <> equipo_visitante)
            );

            CREATE INDEX idx_usuarios_nickname ON usuarios(nickname);
            CREATE INDEX idx_insc_torneo     ON inscripciones(id_torneo);
            CREATE INDEX idx_pagos_torneo    ON pagos(id_torneo);
            """)
            print("🔧 DB creada.")

