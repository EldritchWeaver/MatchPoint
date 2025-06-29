# app/routers/inscriptions.py
from typing import List

import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status

from app.crud import crud_inscription
from app.db.database import get_db
from app.schemas.inscription import Inscripcion, InscripcionCreate

router = APIRouter()


@router.post("/", response_model=Inscripcion)
def create_inscription(inscription: InscripcionCreate, db: sqlite3.Connection = Depends(get_db)):
    db_inscription = crud_inscription.create_inscription(db, inscription=inscription)
    if db_inscription is None:
        raise HTTPException(status_code=400, detail="Invalid inscription data")
    return db_inscription


@router.get("/", response_model=List[Inscripcion])
def read_inscriptions(skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db)):
    inscriptions = crud_inscription.get_inscriptions(db, skip=skip, limit=limit)
    return inscriptions


@router.delete("/{inscription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inscription(inscription_id: int, db: sqlite3.Connection = Depends(get_db)):
    if not crud_inscription.delete_inscription(db, inscription_id=inscription_id):
        raise HTTPException(status_code=404, detail="Inscription not found")

