from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from dependencies import get_db, get_api_key

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=schemas.ProyectoOut, status_code=status.HTTP_201_CREATED)
def create_proyecto(proy: schemas.ProyectoCreate, db: Session = Depends(get_db)):
    db_proyecto = models.Proyecto(**proy.model_dump())
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.get("/", response_model=List[schemas.ProyectoOut])
def read_proyectos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    proyectos = db.query(models.Proyecto).offset(skip).limit(limit).all()
    return proyectos

@router.get("/{id}", response_model=schemas.ProyectoOut)
def read_proyecto(id: int, db: Session = Depends(get_db)):
    proyecto = db.query(models.Proyecto).filter(
        models.Proyecto.id_proyecto == id
    ).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Proyecto no encontrado"
        )
    return proyecto

@router.put("/{id}", response_model=schemas.ProyectoOut)
def update_proyecto(
    id: int, 
    proy: schemas.ProyectoUpdate, 
    db: Session = Depends(get_db)
):
    db_proyecto = db.query(models.Proyecto).filter(
        models.Proyecto.id_proyecto == id
    ).first()
    
    if not db_proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Proyecto no encontrado"
        )
    
    datos_actualizacion = proy.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizacion.items():
        setattr(db_proyecto, campo, valor)
    
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_proyecto(id: int, db: Session = Depends(get_db)):
    db_proyecto = db.query(models.Proyecto).filter(
        models.Proyecto.id_proyecto == id
    ).first()
    
    if not db_proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Proyecto no encontrado"
        )
    
    db.delete(db_proyecto)
    db.commit()