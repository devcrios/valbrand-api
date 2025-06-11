from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from dependencies import get_db, get_api_key
from models import FinancieroPago
from schemas import PagoCreate, PagoOut, PagoUpdate

router = APIRouter(
    prefix="/financiero/pagos",
    tags=["financiero"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=PagoOut, status_code=status.HTTP_201_CREATED)
def create_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    try:
        db_pago = FinancieroPago(**pago.model_dump())
        db.add(db_pago)
        db.commit()
        db.refresh(db_pago)
        return db_pago
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el pago"
        )

@router.get("/", response_model=List[PagoOut])
def list_pagos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        pagos = db.query(FinancieroPago).offset(skip).limit(limit).all()
        return pagos
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener los pagos"
        )

@router.get("/{pago_id}", response_model=PagoOut)
def get_pago(pago_id: int, db: Session = Depends(get_db)):
    if pago_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de pago inválido"
        )
    
    try:
        db_pago = db.get(FinancieroPago, pago_id)
        if not db_pago:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pago no encontrado"
            )
        return db_pago
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener el pago"
        )

@router.put("/{pago_id}", response_model=PagoOut)
def update_pago(pago_id: int, pago_update: PagoUpdate, db: Session = Depends(get_db)):
    if pago_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de pago inválido"
        )
    
    try:
        db_pago = db.get(FinancieroPago, pago_id)
        if not db_pago:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pago no encontrado"
            )
        
        update_data = pago_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron datos para actualizar"
            )
        
        for field, value in update_data.items():
            setattr(db_pago, field, value)
        
        db.commit()
        db.refresh(db_pago)
        return db_pago
        
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el pago"
        )

@router.delete("/{pago_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pago(pago_id: int, db: Session = Depends(get_db)):
    if pago_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de pago inválido"
        )
    
    try:
        db_pago = db.get(FinancieroPago, pago_id)
        if not db_pago:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pago no encontrado"
            )
        
        db.delete(db_pago)
        db.commit()
        
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el pago"
        )