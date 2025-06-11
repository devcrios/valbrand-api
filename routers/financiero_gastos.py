from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from dependencies import get_db, get_api_key
from models import FinancieroGasto
from schemas import GastoCreate, GastoOut, GastoUpdate

router = APIRouter(
    prefix="/financiero/gastos",
    tags=["financiero"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=GastoOut, status_code=status.HTTP_201_CREATED)
def create_gasto(gasto: GastoCreate, db: Session = Depends(get_db)):
    try:
        db_gasto = FinancieroGasto(**gasto.model_dump())
        db.add(db_gasto)
        db.commit()
        db.refresh(db_gasto)
        return db_gasto
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el gasto"
        )

@router.get("/", response_model=List[GastoOut])
def list_gastos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        gastos = db.query(FinancieroGasto).offset(skip).limit(limit).all()
        return gastos
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener los gastos"
        )

@router.get("/{gasto_id}", response_model=GastoOut)
def get_gasto(gasto_id: int, db: Session = Depends(get_db)):
    if gasto_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de gasto inválido"
        )
    
    try:
        db_gasto = db.get(FinancieroGasto, gasto_id)
        if not db_gasto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gasto no encontrado"
            )
        return db_gasto
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener el gasto"
        )

@router.put("/{gasto_id}", response_model=GastoOut)
def update_gasto(gasto_id: int, gasto_update: GastoUpdate, db: Session = Depends(get_db)):
    if gasto_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de gasto inválido"
        )
    
    try:
        db_gasto = db.get(FinancieroGasto, gasto_id)
        if not db_gasto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gasto no encontrado"
            )
        
        update_data = gasto_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron datos para actualizar"
            )
        
        for field, value in update_data.items():
            setattr(db_gasto, field, value)
        
        db.commit()
        db.refresh(db_gasto)
        return db_gasto
        
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el gasto"
        )

@router.delete("/{gasto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gasto(gasto_id: int, db: Session = Depends(get_db)):
    if gasto_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de gasto inválido"
        )
    
    try:
        db_gasto = db.get(FinancieroGasto, gasto_id)
        if not db_gasto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gasto no encontrado"
            )
        
        db.delete(db_gasto)
        db.commit()
        
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el gasto"
        )