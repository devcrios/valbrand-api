from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
import models, schemas
from dependencies import get_db
from dependencies import get_api_key

router = APIRouter(prefix="/ecommerce/proyectos", tags=["E-Commerce Proyectos"], dependencies=[Depends(get_api_key)])

@router.post("/", response_model=schemas.EcommerceProyectoOut)
def create_proyecto(proyecto: schemas.EcommerceProyectoCreate, db: Session = Depends(get_db)):
   db_obj = models.EcommerceProyecto(**proyecto.model_dump())
   db.add(db_obj); db.commit(); db.refresh(db_obj)
   return db_obj

@router.get("/", response_model=List[schemas.EcommerceProyectoOut])
def list_proyectos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
   return db.query(models.EcommerceProyecto).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=schemas.EcommerceProyectoOut)
def get_proyecto(id: int, db: Session = Depends(get_db)):
   obj = db.get(models.EcommerceProyecto, id)
   if not obj:
       raise HTTPException(status_code=404, detail="Proyecto no encontrado")
   return obj

@router.put("/{id}", response_model=schemas.EcommerceProyectoOut)
def update_proyecto(id: int, proyecto: schemas.EcommerceProyectoUpdate, db: Session = Depends(get_db)):
   obj = db.get(models.EcommerceProyecto, id)
   if not obj:
       raise HTTPException(status_code=404, detail="Proyecto no encontrado")
   for k, v in proyecto.model_dump(exclude_unset=True).items(): setattr(obj, k, v)
   db.commit(); db.refresh(obj)
   return obj

@router.delete("/{id}")
def delete_proyecto(id: int, db: Session = Depends(get_db)):
   obj = db.get(models.EcommerceProyecto, id)
   if not obj:
       raise HTTPException(status_code=404, detail="Proyecto no encontrado")
   db.delete(obj); db.commit()
   return {"detail": "Eliminado"}