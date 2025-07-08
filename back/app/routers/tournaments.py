# app/routers/tournaments.py
from typing import List

import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status

from app.crud import crud_tournament
from app.db.database import get_db
from app.schemas.tournament import Torneo, TorneoCreate, TorneoBase, TorneoStatusUpdate

router = APIRouter()


@router.get("/status/{status}", response_model=List[Torneo])
def read_tournaments_by_status(status: str, db: sqlite3.Connection = Depends(get_db)):
    return crud_tournament.get_tournaments_by_status(db, status=status)


@router.post("/", response_model=Torneo)
def create_tournament(tournament: TorneoCreate, db: sqlite3.Connection = Depends(get_db)):
    # Validar unicidad de nombre de torneo
    existing = db.execute("SELECT * FROM torneos WHERE nombre = ?", (tournament.nombre,)).fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="El nombre del torneo ya está registrado")
    return crud_tournament.create_tournament(db=db, tournament=tournament)


@router.get("/", response_model=List[Torneo])
def read_tournaments(skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db)):
    tournaments = crud_tournament.get_tournaments(db, skip=skip, limit=limit)
    return tournaments


@router.get("/{tournament_id}", response_model=Torneo)
def read_tournament(tournament_id: int, db: sqlite3.Connection = Depends(get_db)):
    db_tournament = crud_tournament.get_tournament(db, tournament_id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return db_tournament


@router.put("/{tournament_id}", response_model=Torneo)
def update_tournament(
    tournament_id: int, tournament: TorneoBase, db: sqlite3.Connection = Depends(get_db)
):
    # Validar unicidad de nombre de torneo (excepto para el propio torneo)
    existing = db.execute("SELECT * FROM torneos WHERE nombre = ? AND id != ?", (tournament.nombre, tournament_id)).fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="El nombre del torneo ya está registrado por otro torneo")
    db_tournament = crud_tournament.update_tournament(
        db, tournament_id=tournament_id, tournament=tournament
    )
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return db_tournament


@router.put("/{tournament_id}/status", response_model=Torneo)
def update_tournament_status(tournament_id: int, status_update: TorneoStatusUpdate, db: sqlite3.Connection = Depends(get_db)):
    db_tournament = crud_tournament.update_tournament_status(
        db, tournament_id=tournament_id, status=status_update.status
    )
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return db_tournament
def delete_tournament(tournament_id: int, db: sqlite3.Connection = Depends(get_db)):
    if not crud_tournament.delete_tournament(db, tournament_id=tournament_id):
        raise HTTPException(status_code=404, detail="Tournament not found")

