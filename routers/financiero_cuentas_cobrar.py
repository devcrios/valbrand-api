from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_db, get_api_key
from models import FinancieroCuentaCobrar
from schemas import CuentaCobrarCreate, CuentaCobrarOut, CuentaCobrarUpdate

router = APIRouter(
   prefix="/financiero/cuentas-cobrar",
   tags=["financiero"],
   dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=CuentaCobrarOut, status_code=status.HTTP_201_CREATED)
def create_cuenta(c: CuentaCobrarCreate, db: Session = Depends(get_db)):
   db_c = FinancieroCuentaCobrar(**c.model_dump())
   db.add(db_c); db.commit(); db.refresh(db_c)
   return db_c

@router.get("/", response_model=list[CuentaCobrarOut])
def list_cuentas(db: Session = Depends(get_db)):
   return db.query(FinancieroCuentaCobrar).all()

@router.get("/{cuenta_id}", response_model=CuentaCobrarOut)
def get_cuenta(cuenta_id: int, db: Session = Depends(get_db)):
   db_c = db.get(FinancieroCuentaCobrar, cuenta_id)
   if not db_c:
       raise HTTPException(404, "Cuenta por cobrar no encontrada")
   return db_c

@router.put("/{cuenta_id}", response_model=CuentaCobrarOut)
def update_cuenta(cuenta_id: int, c: CuentaCobrarUpdate, db: Session = Depends(get_db)):
   db_c = db.get(FinancieroCuentaCobrar, cuenta_id)
   if not db_c:
       raise HTTPException(404, "Cuenta por cobrar no encontrada")
   for k, v in c.model_dump(exclude_unset=True).items():
       setattr(db_c, k, v)
   db.commit(); db.refresh(db_c)
   return db_c

@router.delete("/{cuenta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cuenta(cuenta_id: int, db: Session = Depends(get_db)):
   db_c = db.get(FinancieroCuentaCobrar, cuenta_id)
   if not db_c:
       raise HTTPException(404, "Cuenta por cobrar no encontrada")
   db.delete(db_c); db.commit()