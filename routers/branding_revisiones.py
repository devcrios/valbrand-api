from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from dependencies import get_api_key
from models import BrandingRevision
from schemas import RevisionCreate, RevisionOut

router = APIRouter(prefix="/branding/revisiones", tags=["branding_revisiones"], dependencies=[Depends(get_api_key)])

@router.post("/", response_model=RevisionOut, status_code=status.HTTP_201_CREATED)
def create_revision(item: RevisionCreate, db: Session = Depends(get_db)):
   db_obj = BrandingRevision(**item.model_dump())
   db.add(db_obj)
   db.commit()
   db.refresh(db_obj)
   return db_obj

@router.get("/", response_model=List[RevisionOut])
def list_revisiones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
   return db.query(BrandingRevision).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=RevisionOut)
def get_revision(id: int, db: Session = Depends(get_db)):
   obj = db.get(BrandingRevision, id)
   if not obj:
       raise HTTPException(status_code=404, detail="Revisión no encontrada")
   return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_revision(id: int, db: Session = Depends(get_db)):
   obj = db.get(BrandingRevision, id)
   if not obj:
       raise HTTPException(status_code=404, detail="Revisión no encontrada")
   db.delete(obj)
   db.commit()