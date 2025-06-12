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

@router.post("/create-initial-admin", response_model=schemas.Usuario)
def create_initial_admin(db: Session = Depends(get_db)):
    """
    Endpoint temporal para crear el primer usuario administrador
    ⚠️ ELIMINAR DESPUÉS DEL PRIMER USO POR SEGURIDAD
    """
    
    # Verificar si ya existe un administrador
    existing_admin = db.query(models.Usuario).filter(
        models.Usuario.id_rol == 1  # Asumiendo que 1 es rol admin
    ).first()
    
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario administrador en el sistema"
        )
    
    # Datos del admin inicial (CAMBIAR ESTOS VALORES)
    admin_data = {
        "nombre": "Administrador",
        "apellidos": "Sistema",
        "email": "dev.crios@gmail.com",  # ⚠️ CAMBIAR ESTE EMAIL
        "password": "sa1234",         # ⚠️ CAMBIAR ESTA CONTRASEÑA
        "id_rol": 1,                     # Rol de administrador
        "cargo": "Administrador del Sistema",
        "departamento": "IT",
        "telefono": None,
        "configuracion_notificaciones": None,
        "creado_por": None
    }
    
    # Crear usuario
    hashed_password = pwd_context.hash(admin_data["password"])
    user_data_without_password = {k: v for k, v in admin_data.items() if k != "password"}
    
    db_usuario = models.Usuario(
        **user_data_without_password, 
        contrasena=hashed_password
    )
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    
    return db_usuario