# app/routers/teams.py
from typing import List

import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status

from app.crud import crud_team
from app.db.database import get_db
from app.schemas.team import Equipo, EquipoCreate, EquipoBase

router = APIRouter()


@router.post("/", response_model=Equipo)
def create_team(team: EquipoCreate, db: sqlite3.Connection = Depends(get_db)):
    # Validar unicidad de nombre de equipo
    existing_team = db.execute("SELECT * FROM equipos WHERE nombre = ?", (team.nombre,)).fetchone()
    if existing_team:
        raise HTTPException(status_code=400, detail="El nombre del equipo ya está registrado")
    db_team = crud_team.create_team(db, team=team)
    if db_team is None:
        raise HTTPException(status_code=400, detail="El capitán ya lidera otro equipo o datos inválidos")
    return db_team


@router.get("/", response_model=List[Equipo])
def read_teams(skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db)):
    teams = crud_team.get_teams(db, skip=skip, limit=limit)
    return teams


@router.get("/{team_id}", response_model=Equipo)
def read_team(team_id: int, db: sqlite3.Connection = Depends(get_db)):
    db_team = crud_team.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


@router.put("/{team_id}", response_model=Equipo)
def update_team(team_id: int, team: EquipoBase, db: sqlite3.Connection = Depends(get_db)):
    # Validar unicidad de nombre de equipo (excepto para el propio equipo)
    existing_team = db.execute("SELECT * FROM equipos WHERE nombre = ? AND id != ?", (team.nombre, team_id)).fetchone()
    if existing_team:
        raise HTTPException(status_code=400, detail="El nombre del equipo ya está registrado por otro equipo")
    db_team = crud_team.update_team(db, team_id=team_id, team=team)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int, db: sqlite3.Connection = Depends(get_db)):
    if not crud_team.delete_team(db, team_id=team_id):
        raise HTTPException(status_code=404, detail="Team not found")

