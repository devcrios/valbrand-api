from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from dependencies import get_db, get_api_key
import models, schemas

router = APIRouter(
    prefix="/produccion/talleres",
    tags=["produccion", "talleres"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=schemas.TallerOut, status_code=status.HTTP_201_CREATED)
def crear_taller(taller: schemas.TallerCreate, db: Session = Depends(get_db)):
    db_taller = models.ProduccionTaller(**taller.model_dump())
    db.add(db_taller)
    db.commit()
    db.refresh(db_taller)
    return db_taller

@router.get("/", response_model=List[schemas.TallerOut])
def listar_talleres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    talleres = db.query(models.ProduccionTaller).offset(skip).limit(limit).all()
    return talleres

@router.get("/{id_taller}", response_model=schemas.TallerOut)
def obtener_taller(id_taller: int, db: Session = Depends(get_db)):
    taller = db.query(models.ProduccionTaller).filter(
        models.ProduccionTaller.id == id_taller
    ).first()
    
    if not taller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Taller no encontrado"
        )
    return taller

@router.put("/{id_taller}", response_model=schemas.TallerOut)
def actualizar_taller(
    id_taller: int, 
    datos: schemas.TallerUpdate, 
    db: Session = Depends(get_db)
):
    taller = db.query(models.ProduccionTaller).filter(
        models.ProduccionTaller.id == id_taller
    ).first()
    
    if not taller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Taller no encontrado"
        )
    
    datos_actualizacion = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizacion.items():
        setattr(taller, campo, valor)
    
    db.commit()
    db.refresh(taller)
    return taller

@router.delete("/{id_taller}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_taller(id_taller: int, db: Session = Depends(get_db)):
    taller = db.query(models.ProduccionTaller).filter(
        models.ProduccionTaller.id == id_taller
    ).first()
    
    if not taller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Taller no encontrado"
        )
    
    db.delete(taller)
    db.commit()