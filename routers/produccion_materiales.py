from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from dependencies import get_db, get_api_key
import models, schemas

router = APIRouter(
    prefix="/produccion/materiales",
    tags=["produccion", "materiales"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=schemas.MaterialOut, status_code=status.HTTP_201_CREATED)
def crear_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    db_material = models.ProduccionMaterial(**material.model_dump())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

@router.get("/", response_model=List[schemas.MaterialOut])
def listar_materiales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    materiales = db.query(models.ProduccionMaterial).offset(skip).limit(limit).all()
    return materiales

@router.get("/{id_material}", response_model=schemas.MaterialOut)
def obtener_material(id_material: int, db: Session = Depends(get_db)):
    material = db.query(models.ProduccionMaterial).filter(
        models.ProduccionMaterial.id == id_material
    ).first()
    
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Material no encontrado"
        )
    return material

@router.put("/{id_material}", response_model=schemas.MaterialOut)
def actualizar_material(
    id_material: int, 
    datos: schemas.MaterialUpdate, 
    db: Session = Depends(get_db)
):
    material = db.query(models.ProduccionMaterial).filter(
        models.ProduccionMaterial.id == id_material
    ).first()
    
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Material no encontrado"
        )
    
    datos_actualizacion = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizacion.items():
        setattr(material, campo, valor)
    
    db.commit()
    db.refresh(material)
    return material

@router.delete("/{id_material}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_material(id_material: int, db: Session = Depends(get_db)):
    material = db.query(models.ProduccionMaterial).filter(
        models.ProduccionMaterial.id == id_material
    ).first()
    
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Material no encontrado"
        )
    
    db.delete(material)
    db.commit()