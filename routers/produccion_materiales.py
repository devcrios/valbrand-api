from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from dependencies import get_db, get_api_key
import models, schemas

router = APIRouter(
    prefix="/produccion/materiales",
    tags=["produccion","materiales"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=schemas.MaterialOut, status_code=status.HTTP_201_CREATED)
def crear_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    db_m = models.ProduccionMaterial(**material.dict())
    db.add(db_m); db.commit(); db.refresh(db_m)
    return db_m

@router.get("/", response_model=List[schemas.MaterialOut])
def listar_materiales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ProduccionMaterial).offset(skip).limit(limit).all()

@router.get("/{id_material}", response_model=schemas.MaterialOut)
def obtener_material(id_material: int, db: Session = Depends(get_db)):
    m = db.query(models.ProduccionMaterial).get(id_material)
    if not m:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    return m

@router.put("/{id_material}", response_model=schemas.MaterialOut)
def actualizar_material(id_material: int, datos: schemas.MaterialUpdate, db: Session = Depends(get_db)):
    m = db.query(models.ProduccionMaterial).get(id_material)
    if not m:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    for k, v in datos.dict(exclude_unset=True).items(): setattr(m, k, v)
    db.commit(); db.refresh(m)
    return m

@router.delete("/{id_material}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_material(id_material: int, db: Session = Depends(get_db)):
    m = db.query(models.ProduccionMaterial).get(id_material)
    if not m:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    db.delete(m); db.commit()
