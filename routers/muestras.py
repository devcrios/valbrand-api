from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import models, schemas
from dependencies import get_db, get_api_key

router = APIRouter(
    prefix="/muestras", 
    tags=["muestras"], 
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=schemas.MuestraOut, status_code=status.HTTP_201_CREATED)
def create_muestra(muestra: schemas.MuestraCreate, db: Session = Depends(get_db)):
    try:
        db_muestra = models.MolderiaMuestra(**muestra.model_dump())
        db.add(db_muestra)
        db.commit()
        db.refresh(db_muestra)
        return db_muestra
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear la muestra"
        )

@router.get("/", response_model=List[schemas.MuestraOut])
def read_muestras(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Validar parámetros de paginación
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parámetro 'skip' debe ser mayor o igual a 0"
        )
    
    if limit <= 0 or limit > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parámetro 'limit' debe estar entre 1 y 1000"
        )
    
    try:
        muestras = db.query(models.MolderiaMuestra).offset(skip).limit(limit).all()
        return muestras
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener las muestras"
        )

@router.get("/{muestra_id}", response_model=schemas.MuestraOut)
def read_muestra(muestra_id: int, db: Session = Depends(get_db)):
    if muestra_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de muestra inválido"
        )
    
    try:
        db_muestra = db.get(models.MolderiaMuestra, muestra_id)
        if not db_muestra:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Muestra no encontrada"
            )
        return db_muestra
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener la muestra"
        )

@router.put("/{muestra_id}", response_model=schemas.MuestraOut)
def update_muestra(muestra_id: int, muestra_update: schemas.MuestraUpdate, db: Session = Depends(get_db)):
    if muestra_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de muestra inválido"
        )
    
    try:
        db_muestra = db.get(models.MolderiaMuestra, muestra_id)
        if not db_muestra:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Muestra no encontrada"
            )
        
        update_data = muestra_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron datos para actualizar"
            )
        
        for field, value in update_data.items():
            setattr(db_muestra, field, value)
        
        db.commit()
        db.refresh(db_muestra)
        return db_muestra
        
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar la muestra"
        )

@router.delete("/{muestra_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_muestra(muestra_id: int, db: Session = Depends(get_db)):
    if muestra_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de muestra inválido"
        )
    
    try:
        db_muestra = db.get(models.MolderiaMuestra, muestra_id)
        if not db_muestra:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Muestra no encontrada"
            )
        
        db.delete(db_muestra)
        db.commit()
        
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar la muestra"
        )