from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from dependencies import get_db, get_api_key
import models, schemas

router = APIRouter(
    prefix="/produccion/planes",
    tags=["produccion", "planes"],
    dependencies=[Depends(get_api_key)]
)

@router.post(
    "/", 
    response_model=schemas.PlanOut, 
    status_code=status.HTTP_201_CREATED
)
def crear_plan(
    plan: schemas.PlanCreate, 
    db: Session = Depends(get_db)
):
    db_plan = models.ProduccionPlan(**plan.model_dump())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

@router.get(
    "/", 
    response_model=List[schemas.PlanOut]
)
def listar_planes(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return (
        db.query(models.ProduccionPlan)
          .offset(skip)
          .limit(limit)
          .all()
    )

@router.get(
    "/{id_plan}", 
    response_model=schemas.PlanOut
)
def obtener_plan(
    id_plan: int, 
    db: Session = Depends(get_db)
):
    plan = (
        db.query(models.ProduccionPlan)
          .filter(models.ProduccionPlan.id_plan == id_plan)
          .first()
    )
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan no encontrado"
        )
    return plan

@router.put(
    "/{id_plan}", 
    response_model=schemas.PlanOut
)
def actualizar_plan(
    id_plan: int, 
    datos: schemas.PlanUpdate, 
    db: Session = Depends(get_db)
):
    plan = (
        db.query(models.ProduccionPlan)
          .filter(models.ProduccionPlan.id_plan == id_plan)
          .first()
    )
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan no encontrado"
        )

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(plan, campo, valor)

    db.commit()
    db.refresh(plan)
    return plan

@router.delete(
    "/{id_plan}", 
    status_code=status.HTTP_204_NO_CONTENT
)
def borrar_plan(
    id_plan: int, 
    db: Session = Depends(get_db)
):
    plan = (
        db.query(models.ProduccionPlan)
          .filter(models.ProduccionPlan.id_plan == id_plan)
          .first()
    )
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan no encontrado"
        )

    db.delete(plan)
    db.commit()
    # FastAPI con 204_NO_CONTENT no devuelve body
