from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from dependencies import get_api_key
from models import BrandingProyecto
from schemas import BrandingProyectoCreate, BrandingProyectoUpdate, BrandingProyectoOut

router = APIRouter(prefix="/branding/proyectos", tags=["branding_proyectos"], dependencies=[Depends(get_api_key)])

@router.post("/", response_model=BrandingProyectoOut, status_code=status.HTTP_201_CREATED)
def create_proyecto(item: BrandingProyectoCreate, db: Session = Depends(get_db)):
   db_obj = BrandingProyecto(**item.model_dump())
   db.add(db_obj)
   db.commit()
   db.refresh(db_obj)
   return db_obj

@router.get("/", response_model=List[BrandingProyectoOut])
def list_proyectos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
   return db.query(BrandingProyecto).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=BrandingProyectoOut)
def get_proyecto(id: int, db: Session = Depends(get_db)):
   obj = db.get(BrandingProyecto, id)
   if not obj:
       raise HTTPException(status_code=404, detail="Proyecto no encontrado")
   return obj

@router.put("/{id}", response_model=BrandingProyectoOut)
def update_proyecto(id: int, item: BrandingProyectoUpdate, db: Session = Depends(get_db)):
   db_obj = db.get(BrandingProyecto, id)
   if not db_obj:
       raise HTTPException(status_code=404, detail="Proyecto no encontrado")
   for k, v in item.model_dump(exclude_unset=True).items():
       setattr(db_obj, k, v)
   db.commit()
   db.refresh(db_obj)
   return db_obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_proyecto(id: int, db: Session = Depends(get_db)):
   db_obj = db.get(BrandingProyecto, id)
   if not db_obj:
       raise HTTPException(status_code=404, detail="Proyecto no encontrado")
   db.delete(db_obj)
   db.commit()