from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
import models, schemas
from dependencies import get_db
from dependencies import get_api_key

router = APIRouter(prefix="/ecommerce/credenciales", tags=["E-Commerce Credenciales"], dependencies=[Depends(get_api_key)])

@router.post("/", response_model=schemas.EcommerceCredencialOut)
def create_credencial(c: schemas.EcommerceCredencialCreate, db: Session = Depends(get_db)):
   db_obj = models.EcommerceCredencial(**c.model_dump())
   db.add(db_obj); db.commit(); db.refresh(db_obj)
   return db_obj

@router.get("/", response_model=List[schemas.EcommerceCredencialOut])
def list_credenciales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
   return db.query(models.EcommerceCredencial).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=schemas.EcommerceCredencialOut)
def get_credencial(id: int, db: Session = Depends(get_db)):
   obj = db.get(models.EcommerceCredencial, id)
   if not obj: raise HTTPException(404, "No encontrada")
   return obj

@router.put("/{id}", response_model=schemas.EcommerceCredencialOut)
def update_credencial(id: int, c: schemas.EcommerceCredencialUpdate, db: Session = Depends(get_db)):
   obj = db.get(models.EcommerceCredencial, id)
   if not obj: raise HTTPException(404, "No encontrada")
   for k, v in c.model_dump(exclude_unset=True).items(): setattr(obj, k, v)
   db.commit(); db.refresh(obj)
   return obj

@router.delete("/{id}")
def delete_credencial(id: int, db: Session = Depends(get_db)):
   obj = db.get(models.EcommerceCredencial, id)
   if not obj: raise HTTPException(404, "No encontrada")
   db.delete(obj); db.commit()
   return {"detail": "Eliminada"}