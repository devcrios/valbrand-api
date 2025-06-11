from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from dependencies import get_db, get_api_key
import models, schemas

router = APIRouter(
    prefix="/produccion/etapas",
    tags=["produccion", "etapas"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=schemas.EtapaOut, status_code=status.HTTP_201_CREATED)
def crear_etapa(etapa: schemas.EtapaCreate, db: Session = Depends(get_db)):
    db_etapa = models.ProduccionEtapa(**etapa.model_dump())
    db.add(db_etapa)
    db.commit()
    db.refresh(db_etapa)
    return db_etapa

@router.get("/", response_model=List[schemas.EtapaOut])
def listar_etapas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    etapas = db.query(models.ProduccionEtapa).offset(skip).limit(limit).all()
    return etapas

@router.get("/{id_etapa}", response_model=schemas.EtapaOut)
def obtener_etapa(id_etapa: int, db: Session = Depends(get_db)):
    etapa = db.query(models.ProduccionEtapa).filter(
        models.ProduccionEtapa.id == id_etapa
    ).first()
    
    if not etapa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Etapa no encontrada"
        )
    return etapa

@router.put("/{id_etapa}", response_model=schemas.EtapaOut)
def actualizar_etapa(
    id_etapa: int, 
    datos: schemas.EtapaUpdate, 
    db: Session = Depends(get_db)
):
    etapa = db.query(models.ProduccionEtapa).filter(
        models.ProduccionEtapa.id == id_etapa
    ).first()
    
    if not etapa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Etapa no encontrada"
        )
    
    datos_actualizacion = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizacion.items():
        setattr(etapa, campo, valor)
    
    db.commit()
    db.refresh(etapa)
    return etapa

@router.delete("/{id_etapa}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_etapa(id_etapa: int, db: Session = Depends(get_db)):
    etapa = db.query(models.ProduccionEtapa).filter(
        models.ProduccionEtapa.id == id_etapa
    ).first()
    
    if not etapa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Etapa no encontrada"
        )
    
    db.delete(etapa)
    db.commit()