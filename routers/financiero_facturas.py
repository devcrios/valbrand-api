from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from dependencies import get_db, get_api_key
from models import FinancieroFactura
from schemas import FacturaCreate, FacturaOut, FacturaUpdate

router = APIRouter(
    prefix="/financiero/facturas",
    tags=["financiero"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=FacturaOut, status_code=status.HTTP_201_CREATED)
def create_factura(factura: FacturaCreate, db: Session = Depends(get_db)):
    try:
        db_factura = FinancieroFactura(**factura.model_dump())
        db.add(db_factura)
        db.commit()
        db.refresh(db_factura)
        return db_factura
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear la factura"
        )

@router.get("/", response_model=List[FacturaOut])
def list_facturas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        facturas = db.query(FinancieroFactura).offset(skip).limit(limit).all()
        return facturas
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener las facturas"
        )

@router.get("/{factura_id}", response_model=FacturaOut)
def get_factura(factura_id: int, db: Session = Depends(get_db)):
    if factura_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de factura inválido"
        )
    
    try:
        db_factura = db.get(FinancieroFactura, factura_id)
        if not db_factura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Factura no encontrada"
            )
        return db_factura
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener la factura"
        )

@router.put("/{factura_id}", response_model=FacturaOut)
def update_factura(factura_id: int, factura_update: FacturaUpdate, db: Session = Depends(get_db)):
    if factura_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de factura inválido"
        )
    
    try:
        db_factura = db.get(FinancieroFactura, factura_id)
        if not db_factura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Factura no encontrada"
            )
        
        update_data = factura_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron datos para actualizar"
            )
        
        for field, value in update_data.items():
            setattr(db_factura, field, value)
        
        db.commit()
        db.refresh(db_factura)
        return db_factura
        
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar la factura"
        )

@router.delete("/{factura_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_factura(factura_id: int, db: Session = Depends(get_db)):
    if factura_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de factura inválido"
        )
    
    try:
        db_factura = db.get(FinancieroFactura, factura_id)
        if not db_factura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Factura no encontrada"
            )
        
        db.delete(db_factura)
        db.commit()
        
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar la factura"
        )