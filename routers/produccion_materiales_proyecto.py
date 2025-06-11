from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from dependencies import get_db, get_api_key
import models, schemas

router = APIRouter(
    prefix="/produccion/materiales_proyecto",
    tags=["produccion", "materiales_proyecto"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=schemas.MatProyectoOut, status_code=status.HTTP_201_CREATED)
def crear_mat_proy(mat: schemas.MatProyectoCreate, db: Session = Depends(get_db)):
    db_material_proyecto = models.ProduccionMaterialProyecto(**mat.model_dump())
    db.add(db_material_proyecto)
    db.commit()
    db.refresh(db_material_proyecto)
    return db_material_proyecto

@router.get("/", response_model=List[schemas.MatProyectoOut])
def listar_mat_proy(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    materiales_proyecto = db.query(models.ProduccionMaterialProyecto).offset(skip).limit(limit).all()
    return materiales_proyecto

@router.get("/{id_mat_proy}", response_model=schemas.MatProyectoOut)
def obtener_mat_proy(id_mat_proy: int, db: Session = Depends(get_db)):
    material_proyecto = db.query(models.ProduccionMaterialProyecto).filter(
        models.ProduccionMaterialProyecto.id == id_mat_proy
    ).first()
    
    if not material_proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="MaterialProyecto no encontrado"
        )
    return material_proyecto

@router.put("/{id_mat_proy}", response_model=schemas.MatProyectoOut)
def actualizar_mat_proy(
    id_mat_proy: int, 
    datos: schemas.MatProyectoUpdate, 
    db: Session = Depends(get_db)
):
    material_proyecto = db.query(models.ProduccionMaterialProyecto).filter(
        models.ProduccionMaterialProyecto.id == id_mat_proy
    ).first()
    
    if not material_proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="MaterialProyecto no encontrado"
        )
    
    datos_actualizacion = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizacion.items():
        setattr(material_proyecto, campo, valor)
    
    db.commit()
    db.refresh(material_proyecto)
    return material_proyecto

@router.delete("/{id_mat_proy}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_mat_proy(id_mat_proy: int, db: Session = Depends(get_db)):
    material_proyecto = db.query(models.ProduccionMaterialProyecto).filter(
        models.ProduccionMaterialProyecto.id == id_mat_proy
    ).first()
    
    if not material_proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="MaterialProyecto no encontrado"
        )
    
    db.delete(material_proyecto)
    db.commit()