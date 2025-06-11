from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from typing import List
from sqlalchemy.orm import Session
import models, schemas
from dependencies import get_db
from dependencies import get_api_key

router = APIRouter(prefix="/ecommerce/documentos", tags=["E-Commerce Documentos"], dependencies=[Depends(get_api_key)])

@router.post("/", response_model=schemas.EcommerceDocumentoOut)
def upload_documento(
   id_proyecto_ecommerce: int,
   nombre_documento: str,
   tipo_documento: str,
   descripcion: str = None,
   version: str = None,
   es_publico: bool = False,
   subido_por: int = None,
   file: UploadFile = File(...),
   db: Session = Depends(get_db)
):
   content = file.file.read()
   ext = file.filename.split('.')[-1]
   obj = models.EcommerceDocumento(
       id_proyecto_ecommerce=id_proyecto_ecommerce,
       nombre_documento=nombre_documento,
       tipo_documento=tipo_documento,
       descripcion=descripcion,
       archivo=content,
       nombre_archivo=file.filename,
       extension=ext,
       tamano_archivo=len(content),
       version=version or "1.0",
       es_publico=es_publico,
       subido_por=subido_por
   )
   db.add(obj); db.commit(); db.refresh(obj)
   return obj

@router.get("/", response_model=List[schemas.EcommerceDocumentoOut])
def list_documentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
   return db.query(models.EcommerceDocumento).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=schemas.EcommerceDocumentoOut)
def get_documento(id: int, db: Session = Depends(get_db)):
   obj = db.get(models.EcommerceDocumento, id)
   if not obj: raise HTTPException(404, "No encontrado")
   return obj

@router.delete("/{id}")
def delete_documento(id: int, db: Session = Depends(get_db)):
   obj = db.get(models.EcommerceDocumento, id)
   if not obj: raise HTTPException(404, "No encontrado")
   db.delete(obj); db.commit()
   return {"detail": "Eliminado"}