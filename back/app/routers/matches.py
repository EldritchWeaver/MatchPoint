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


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(match_id: int, db: sqlite3.Connection = Depends(get_db)):
    if not crud_match.delete_match(db, match_id=match_id):
        raise HTTPException(status_code=404, detail="Match not found")

