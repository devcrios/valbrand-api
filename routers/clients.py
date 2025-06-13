from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from dependencies import get_db, get_api_key

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = models.CRMCliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.get("/", response_model=List[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.CRMCliente).offset(skip).limit(limit).all()

@router.get("/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(models.CRMCliente).filter(
        models.CRMCliente.id_cliente == cliente_id
    ).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_cliente

@router.put("/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(
    cliente_id: int, 
    cliente: schemas.ClienteUpdate, 
    db: Session = Depends(get_db)
):
    db_cliente = db.query(models.CRMCliente).filter(
        models.CRMCliente.id_cliente == cliente_id
    ).first()
    
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    
    # Usar exclude_unset=True para solo actualizar campos enviados
    cliente_data = cliente.model_dump(exclude_unset=True)
    
    for field, value in cliente_data.items():
        setattr(db_cliente, field, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.patch("/{cliente_id}", response_model=schemas.Cliente)
def patch_cliente(
    cliente_id: int, 
    cliente: schemas.ClienteUpdate, 
    db: Session = Depends(get_db)
):
    """Endpoint alternativo usando PATCH para actualizaciones parciales"""
    db_cliente = db.query(models.CRMCliente).filter(
        models.CRMCliente.id_cliente == cliente_id
    ).first()
    
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    
    cliente_data = cliente.model_dump(exclude_unset=True, exclude_none=True)
    
    for field, value in cliente_data.items():
        setattr(db_cliente, field, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.delete("/{cliente_id}", status_code=204)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(models.CRMCliente).filter(
        models.CRMCliente.id_cliente == cliente_id
    ).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    
    db.delete(db_cliente)
    db.commit()