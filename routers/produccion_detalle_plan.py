from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from dependencies import get_db, get_api_key
import models, schemas

router = APIRouter(
    prefix="/produccion/detalle_plan",
    tags=["produccion", "detalle_plan"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=schemas.DetallePlanOut, status_code=status.HTTP_201_CREATED)
def crear_detalle(detalle: schemas.DetallePlanCreate, db: Session = Depends(get_db)):
    try:
        db_detalle = models.ProduccionDetallePlan(**detalle.model_dump())
        db.add(db_detalle)
        db.commit()
        db.refresh(db_detalle)
        return db_detalle
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el detalle del plan"
        )

@router.get("/", response_model=List[schemas.DetallePlanOut])
def listar_detalles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
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
        detalles = db.query(models.ProduccionDetallePlan).offset(skip).limit(limit).all()
        return detalles
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener los detalles del plan"
        )

@router.get("/{id_detalle}", response_model=schemas.DetallePlanOut)
def obtener_detalle(id_detalle: int, db: Session = Depends(get_db)):
    if id_detalle <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de detalle inválido"
        )
    
    try:
        db_detalle = db.get(models.ProduccionDetallePlan, id_detalle)
        if not db_detalle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle no encontrado"
            )
        return db_detalle
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener el detalle"
        )

@router.put("/{id_detalle}", response_model=schemas.DetallePlanOut)
def actualizar_detalle(id_detalle: int, detalle_update: schemas.DetallePlanUpdate, db: Session = Depends(get_db)):
    if id_detalle <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de detalle inválido"
        )
    
    try:
        db_detalle = db.get(models.ProduccionDetallePlan, id_detalle)
        if not db_detalle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle no encontrado"
            )
        
        update_data = detalle_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron datos para actualizar"
            )
        
        for field, value in update_data.items():
            setattr(db_detalle, field, value)
        
        db.commit()
        db.refresh(db_detalle)
        return db_detalle
        
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el detalle"
        )

@router.delete("/{id_detalle}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_detalle(id_detalle: int, db: Session = Depends(get_db)):
    if id_detalle <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de detalle inválido"
        )
    
    try:
        db_detalle = db.get(models.ProduccionDetallePlan, id_detalle)
        if not db_detalle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle no encontrado"
            )
        
        db.delete(db_detalle)
        db.commit()
        
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el detalle"
        )