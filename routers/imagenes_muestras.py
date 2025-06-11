from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
import models, schemas
from dependencies import get_db, get_api_key

router = APIRouter(
    prefix="/imagenes-muestras", 
    tags=["imagenes-muestras"], 
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=schemas.ImagenMuestraOut, status_code=status.HTTP_201_CREATED)
def upload_imagen(
    imagen: UploadFile = File(...),
    id_muestra: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    # Validar tipo de archivo
    if not imagen.content_type or not imagen.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser una imagen válida"
        )
    
    # Validar tamaño del archivo (ejemplo: máximo 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    if imagen.size and imagen.size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="El archivo es demasiado grande. Máximo 10MB permitido"
        )
    
    # Validar ID de muestra si se proporciona
    if id_muestra is not None and id_muestra <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de muestra inválido"
        )
    
    try:
        content = imagen.file.read()
        
        # Validar que el contenido no esté vacío
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo está vacío"
            )
        
        db_imagen = models.MolderiaImagenMuestra(
            id_muestra=id_muestra,
            nombre_imagen=imagen.filename,
            imagen=content
        )
        
        db.add(db_imagen)
        db.commit()
        db.refresh(db_imagen)
        return db_imagen
        
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al guardar la imagen"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar el archivo"
        )

@router.get("/", response_model=List[schemas.ImagenMuestraOut])
def list_imagenes(
    skip: int = 0, 
    limit: int = 100, 
    id_muestra: Optional[int] = None,
    db: Session = Depends(get_db)
):
    # Validar parámetros de paginación
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parámetro 'skip' debe ser mayor o igual a 0"
        )
    
    if limit <= 0 or limit > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parámetro 'limit' debe estar entre 1 y 1000"
        )
    
    # Validar ID de muestra si se filtra
    if id_muestra is not None and id_muestra <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de muestra inválido para filtro"
        )
    
    try:
        query = db.query(models.MolderiaImagenMuestra)
        
        # Aplicar filtro por ID de muestra si se especifica
        if id_muestra is not None:
            query = query.filter(models.MolderiaImagenMuestra.id_muestra == id_muestra)
        
        imagenes = query.offset(skip).limit(limit).all()
        return imagenes
        
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener las imágenes"
        )

@router.get("/{imagen_id}", response_model=schemas.ImagenMuestraOut)
def get_imagen(imagen_id: int, db: Session = Depends(get_db)):
    if imagen_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de imagen inválido"
        )
    
    try:
        db_imagen = db.get(models.MolderiaImagenMuestra, imagen_id)
        if not db_imagen:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Imagen no encontrada"
            )
        return db_imagen
        
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener la imagen"
        )

@router.delete("/{imagen_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_imagen(imagen_id: int, db: Session = Depends(get_db)):
    if imagen_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de imagen inválido"
        )
    
    try:
        db_imagen = db.get(models.MolderiaImagenMuestra, imagen_id)
        if not db_imagen:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Imagen no encontrada"
            )
        
        db.delete(db_imagen)
        db.commit()
        
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar la imagen"
        )