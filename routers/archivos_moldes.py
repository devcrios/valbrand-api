from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from dependencies import get_db, get_api_key

router = APIRouter(prefix="/archivos-moldes", tags=["archivos-moldes"], dependencies=[Depends(get_api_key)])

@router.post("/", response_model=schemas.ArchivoMoldeOut)
def upload_archivo(archivo: UploadFile=File(...), id_molde: int=None, db: Session=Depends(get_db)):
    content = archivo.file.read()
    ext = archivo.filename.rsplit('.', 1)[-1].upper()
    
    # Get the enum class from the model field
    tipo_archivo_field = schemas.ArchivoMoldeOut.model_fields['tipo_archivo']
    valid_types = list(tipo_archivo_field.annotation.__members__.keys())
    
    if ext not in valid_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    db_arch = models.MolderiaArchivo(
        id_molde=id_molde,
        nombre_archivo=archivo.filename,
        tipo_archivo=ext,
        archivo=content
    )
    db.add(db_arch)
    db.commit()
    db.refresh(db_arch)
    return db_arch

@router.get("/", response_model=List[schemas.ArchivoMoldeOut])
def list_archivos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.MolderiaArchivo).offset(skip).limit(limit).all()