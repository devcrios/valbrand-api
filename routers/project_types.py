from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from dependencies import get_db, get_api_key

router = APIRouter(
    prefix="/project-types",
    tags=["project-types"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=schemas.ProyectoTipoOut, status_code=status.HTTP_201_CREATED)
def create_tipo(tipo: schemas.ProyectoTipoCreate, db: Session = Depends(get_db)):
    db_tipo = models.ProyectoTipo(**tipo.model_dump())
    db.add(db_tipo)
    db.commit()
    db.refresh(db_tipo)
    return db_tipo

@router.get("/", response_model=List[schemas.ProyectoTipoOut])
def read_tipos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tipos = db.query(models.ProyectoTipo).offset(skip).limit(limit).all()
    return tipos

@router.get("/{id}", response_model=schemas.ProyectoTipoOut)
def get_tipo(id: int, db: Session = Depends(get_db)):
    tipo = db.query(models.ProyectoTipo).filter(
        models.ProyectoTipo.id_tipo_proyecto == id
    ).first()
    
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tipo no encontrado"
        )
    return tipo

@router.put("/{id}", response_model=schemas.ProyectoTipoOut)
def update_tipo(
    id: int, 
    tipo: schemas.ProyectoTipoUpdate, 
    db: Session = Depends(get_db)
):
    db_tipo = db.query(models.ProyectoTipo).filter(
        models.ProyectoTipo.id_tipo_proyecto == id
    ).first()
    
    if not db_tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tipo no encontrado"
        )
    
    datos_actualizacion = tipo.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizacion.items():
        setattr(db_tipo, campo, valor)
    
    db.commit()
    db.refresh(db_tipo)
    return db_tipo

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tipo(id: int, db: Session = Depends(get_db)):
    db_tipo = db.query(models.ProyectoTipo).filter(
        models.ProyectoTipo.id_tipo_proyecto == id
    ).first()
    
    if not db_tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tipo no encontrado"
        )
    
    db.delete(db_tipo)
    db.commit()