
from fastapi import FastAPI

from app.db.database import initialize_database
from app.routers import users, teams, tournaments, inscriptions, payments, matches, members


app = FastAPI(
    title="Torneo API",
    version="1.0.0",
    description="""
    Esta API permite la gestión completa de un sistema de torneos.
    Incluye funcionalidades para administrar:

    - **Usuarios**: Registro, consulta, actualización y eliminación de participantes.
    - **Equipos**: Creación, consulta, modificación y borrado de equipos, con asignación de capitán.
    - **Miembros de Equipo**: Asociación de usuarios a equipos con roles específicos (jugador, capitán, suplente).
    - **Torneos**: Configuración detallada de torneos, incluyendo fechas, descripciones y capacidad máxima de equipos.
    - **Inscripciones**: Gestión de la participación de equipos en torneos.
    - **Pagos**: Registro de pagos asociados a las inscripciones de equipos.
    - **Partidos**: Programación y registro de resultados de los encuentros dentro de los torneos.

    La base de datos utilizada es SQLite, y se inicializa automáticamente si no existe.
    """,
    openapi_tags=[
        {"name": "Users", "description": "Operaciones relacionadas con la gestión de usuarios."},
        {"name": "Teams", "description": "Operaciones relacionadas con la gestión de equipos."},
        {"name": "Members", "description": "Operaciones para gestionar la pertenencia de usuarios a equipos."},
        {"name": "Tournaments", "description": "Operaciones para crear y administrar torneos."},
        {"name": "Inscriptions", "description": "Operaciones para gestionar la inscripción de equipos en torneos."},
        {"name": "Payments", "description": "Operaciones para registrar y consultar pagos de torneos."},
        {"name": "Matches", "description": "Operaciones para programar y gestionar partidos de torneos."},
    ]
)

# Endpoint raíz para mensaje de bienvenida
@app.get("/")
def root():
    return {"message": "Bienvenido a la API de MatchPoint"}

@app.on_event("startup")
def on_startup():
    initialize_database()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(teams.router, prefix="/teams", tags=["Teams"])
app.include_router(members.router, prefix="/members", tags=["Members"])
app.include_router(tournaments.router, prefix="/tournaments", tags=["Tournaments"])
app.include_router(inscriptions.router, prefix="/inscriptions", tags=["Inscriptions"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])
app.include_router(matches.router, prefix="/matches", tags=["Matches"])
