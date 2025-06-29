# app/routers/payments.py
from typing import List

import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status

from app.crud import crud_payment
from app.db.database import get_db
from app.schemas.payment import Pago, PagoCreate

router = APIRouter()


@router.post("/", response_model=Pago)
def create_payment(payment: PagoCreate, db: sqlite3.Connection = Depends(get_db)):
    db_payment = crud_payment.create_payment(db, payment=payment)
    if db_payment is None:
        raise HTTPException(status_code=400, detail="Invalid payment data")
    return db_payment


@router.get("/", response_model=List[Pago])
def read_payments(skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db)):
    payments = crud_payment.get_payments(db, skip=skip, limit=limit)
    return payments


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: int, db: sqlite3.Connection = Depends(get_db)):
    if not crud_payment.delete_payment(db, payment_id=payment_id):
        raise HTTPException(status_code=404, detail="Payment not found")

