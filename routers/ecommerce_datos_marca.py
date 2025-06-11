from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
import models, schemas
from dependencies import get_db
from dependencies import get_api_key

router = APIRouter(prefix="/ecommerce/datos-marca", tags=["E-Commerce Datos Marca"], dependencies=[Depends(get_api_key)])

@router.post("/", response_model=schemas.EcommerceDatosMarcaOut)
def create_datos(d: schemas.EcommerceDatosMarcaCreate, db: Session = Depends(get_db)):
   obj = models.EcommerceDatosMarca(**d.model_dump())
   db.add(obj); db.commit(); db.refresh(obj)
   return obj

@router.get("/", response_model=List[schemas.EcommerceDatosMarcaOut])
def list_datos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
   return db.query(models.EcommerceDatosMarca).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=schemas.EcommerceDatosMarcaOut)
def get_datos(id: int, db: Session = Depends(get_db)):
   obj = db.get(models.EcommerceDatosMarca, id)
   if not obj: raise HTTPException(404, "No encontrado")
   return obj

@router.put("/{id}", response_model=schemas.EcommerceDatosMarcaOut)
def update_datos(id: int, d: schemas.EcommerceDatosMarcaUpdate, db: Session = Depends(get_db)):
   obj = db.get(models.EcommerceDatosMarca, id)
   if not obj: raise HTTPException(404, "No encontrado")
   for k, v in d.model_dump(exclude_unset=True).items(): setattr(obj, k, v)
   db.commit(); db.refresh(obj)
   return obj

@router.delete("/{id}")
def delete_datos(id: int, db: Session = Depends(get_db)):
   obj = db.get(models.EcommerceDatosMarca, id)
   if not obj: raise HTTPException(404, "No encontrado")
   db.delete(obj); db.commit()
   return {"detail": "Eliminado"}