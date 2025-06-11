from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from dependencies import get_api_key
from models import BrandingEntregable
from schemas import EntregableCreate, EntregableOut

router = APIRouter(prefix="/branding/entregables", tags=["branding_entregables"], dependencies=[Depends(get_api_key)])

@router.post("/", response_model=EntregableOut, status_code=status.HTTP_201_CREATED)
def create_entregable(item: EntregableCreate, db: Session = Depends(get_db)):
   db_obj = BrandingEntregable(**item.model_dump())
   db.add(db_obj)
   db.commit()
   db.refresh(db_obj)
   return db_obj

@router.get("/", response_model=List[EntregableOut])
def list_entregables(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
   return db.query(BrandingEntregable).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=EntregableOut)
def get_entregable(id: int, db: Session = Depends(get_db)):
   obj = db.get(BrandingEntregable, id)
   if not obj:
       raise HTTPException(status_code=404, detail="Entregable no encontrado")
   return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entregable(id: int, db: Session = Depends(get_db)):
   obj = db.get(BrandingEntregable, id)
   if not obj:
       raise HTTPException(status_code=404, detail="Entregable no encontrado")
   db.delete(obj)
   db.commit()
