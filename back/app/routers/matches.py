# app/routers/matches.py
from typing import List

import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status

from app.crud import crud_match
from app.db.database import get_db
from app.schemas.match import Partido, PartidoCreate

router = APIRouter()


@router.post("/", response_model=Partido)
def create_match(match: PartidoCreate, db: sqlite3.Connection = Depends(get_db)):
    db_match = crud_match.create_match(db, match=match)
    if db_match is None:
        raise HTTPException(status_code=400, detail="Invalid match data")
    return db_match


@router.get("/", response_model=List[Partido])
def read_matches(skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db)):
    matches = crud_match.get_matches(db, skip=skip, limit=limit)
    return matches


@router.put("/{match_id}", response_model=Partido)
def update_match_result(match_id: int, results: dict, db: sqlite3.Connection = Depends(get_db)):
    resultado_local = results.get('resultado_local')
    resultado_visitante = results.get('resultado_visitante')
    db_match = crud_match.update_match_result(db, match_id=match_id, resultado_local=resultado_local, resultado_visitante=resultado_visitante)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match
def delete_match(match_id: int, db: sqlite3.Connection = Depends(get_db)):
    if not crud_match.delete_match(db, match_id=match_id):
        raise HTTPException(status_code=404, detail="Match not found")

