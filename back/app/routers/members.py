# app/routers/members.py
from typing import List

import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status

from app.crud import crud_member
from app.db.database import get_db
from app.schemas.member import Miembro, MiembroCreate

router = APIRouter()


@router.post("/", response_model=Miembro)
def add_member(member: MiembroCreate, db: sqlite3.Connection = Depends(get_db)):
    db_member = crud_member.add_member(db, member=member)
    if db_member is None:
        raise HTTPException(status_code=400, detail="Invalid member data")
    return db_member


@router.get("/", response_model=List[Miembro])
def read_members(skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db)):
    members = crud_member.get_members(db, skip=skip, limit=limit)
    return members


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: sqlite3.Connection = Depends(get_db)):
    if not crud_member.delete_member(db, member_id=member_id):
        raise HTTPException(status_code=404, detail="Member not found")

