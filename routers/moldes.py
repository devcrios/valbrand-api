from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import models, schemas
from dependencies import get_db, get_api_key

router = APIRouter(
    prefix="/moldes", 
    tags=["moldes"], 
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=schemas.MoldeOut, status_code=status.HTTP_201_CREATED)
def create_molde(molde: schemas.MoldeCreate, db: Session = Depends(get_db)):
    try:
        db_molde = models.MolderiaMolde(**molde.model_dump())
        db.add(db_molde)
        db.commit()
        db.refresh(db_molde)
        return db_molde
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el molde"
        )

@router.get("/", response_model=List[schemas.MoldeOut])
def read_moldes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
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
        moldes = db.query(models.MolderiaMolde).offset(skip).limit(limit).all()
        return moldes
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener los moldes"
        )

@router.get("/{molde_id}", response_model=schemas.MoldeOut)
def read_molde(molde_id: int, db: Session = Depends(get_db)):
    if molde_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de molde inválido"
        )
    
    try:
        db_molde = db.get(models.MolderiaMolde, molde_id)
        if not db_molde:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Molde no encontrado"
            )
        return db_molde
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener el molde"
        )

@router.put("/{molde_id}", response_model=schemas.MoldeOut)
def update_molde(molde_id: int, molde_update: schemas.MoldeUpdate, db: Session = Depends(get_db)):
    if molde_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de molde inválido"
        )
    
    try:
        db_molde = db.get(models.MolderiaMolde, molde_id)
        if not db_molde:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Molde no encontrado"
            )
        
        update_data = molde_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron datos para actualizar"
            )
        
        for field, value in update_data.items():
            setattr(db_molde, field, value)
        
        db.commit()
        db.refresh(db_molde)
        return db_molde
        
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el molde"
        )

@router.delete("/{molde_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_molde(molde_id: int, db: Session = Depends(get_db)):
    if molde_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de molde inválido"
        )
    
    try:
        db_molde = db.get(models.MolderiaMolde, molde_id)
        if not db_molde:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Molde no encontrado"
            )
        
        db.delete(db_molde)
        db.commit()
        
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el molde"
        )