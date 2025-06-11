from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
import models, schemas
from dependencies import get_db, get_api_key

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=schemas.Usuario, status_code=status.HTTP_201_CREATED)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(usuario.password)
    user_data = usuario.model_dump(exclude={"password"})
    db_usuario = models.Usuario(**user_data, contrasena=hashed_password)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.get("/", response_model=List[schemas.Usuario])
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).offset(skip).limit(limit).all()
    return usuarios

@router.get("/{user_id}", response_model=schemas.Usuario)
def read_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == user_id
    ).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    return usuario

@router.put("/{user_id}", response_model=schemas.Usuario)
def update_usuario(
    user_id: int, 
    usuario: schemas.UsuarioUpdate, 
    db: Session = Depends(get_db)
):
    db_usuario = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == user_id
    ).first()
    
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    
    datos_actualizacion = usuario.model_dump(exclude_unset=True)
    
    if "password" in datos_actualizacion:
        datos_actualizacion["contrasena"] = pwd_context.hash(
            datos_actualizacion.pop("password")
        )
    
    for campo, valor in datos_actualizacion.items():
        setattr(db_usuario, campo, valor)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(user_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == user_id
    ).first()
    
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    
    db.delete(db_usuario)
    db.commit()