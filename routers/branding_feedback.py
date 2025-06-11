from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from dependencies import get_api_key
from models import BrandingFeedbackFecha
from schemas import FeedbackFechaCreate, FeedbackFechaOut

router = APIRouter(prefix="/branding/feedback", tags=["branding_feedback"], dependencies=[Depends(get_api_key)])

@router.post("/", response_model=FeedbackFechaOut, status_code=status.HTTP_201_CREATED)
def create_feedback(item: FeedbackFechaCreate, db: Session = Depends(get_db)):
   db_obj = BrandingFeedbackFecha(**item.model_dump())
   db.add(db_obj)
   db.commit()
   db.refresh(db_obj)
   return db_obj

@router.get("/", response_model=List[FeedbackFechaOut])
def list_feedback(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
   return db.query(BrandingFeedbackFecha).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=FeedbackFechaOut)
def get_feedback(id: int, db: Session = Depends(get_db)):
   obj = db.get(BrandingFeedbackFecha, id)
   if not obj:
       raise HTTPException(status_code=404, detail="Feedback no encontrado")
   return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_feedback(id: int, db: Session = Depends(get_db)):
   obj = db.get(BrandingFeedbackFecha, id)
   if not obj:
       raise HTTPException(status_code=404, detail="Feedback no encontrado")
   db.delete(obj)
   db.commit()