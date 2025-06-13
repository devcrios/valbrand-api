from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from dependencies import get_db, get_api_key
import models, schemas
import json

router = APIRouter(
    prefix="/produccion/talleres",
    tags=["produccion", "talleres"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=schemas.TallerOut, status_code=status.HTTP_201_CREATED)
def crear_taller(taller: schemas.TallerCreate, db: Session = Depends(get_db)):
    print(f"=== CREANDO NUEVO TALLER ===")
    
    # Log de datos recibidos
    try:
        datos_recibidos = taller.model_dump()
        print(f"Datos recibidos: {json.dumps(datos_recibidos, indent=2, default=str)}")
    except Exception as e:
        print(f"Error al serializar datos recibidos: {e}")
        print(f"Datos recibidos (raw): {taller}")
    
    # Log de validación del schema
    print(f"Tipo de schema recibido: {type(taller)}")
    print(f"Campos del schema: {list(taller.model_fields.keys()) if hasattr(taller, 'model_fields') else 'No disponible'}")
    
    try:
        # Crear el objeto de base de datos
        print("Creando objeto ProduccionTaller...")
        db_taller = models.ProduccionTaller(**taller.model_dump())
        print(f"Objeto creado exitosamente: {type(db_taller)}")
        
        # Log de los datos que se van a insertar
        print("Datos a insertar en la BD:")
        for campo, valor in taller.model_dump().items():
            print(f"  {campo}: {valor} (tipo: {type(valor)})")
        
        # Intentar guardar en la base de datos
        print("Agregando objeto a la sesión de BD...")
        db.add(db_taller)
        
        print("Ejecutando commit...")
        db.commit()
        
        print("Ejecutando refresh...")
        db.refresh(db_taller)
        
        print(f"Taller creado exitosamente con ID: {db_taller.id}")
        
        # Log del objeto retornado
        print("Datos del taller creado:")
        for column in db_taller.__table__.columns:
            valor = getattr(db_taller, column.name)
            print(f"  {column.name}: {valor} (tipo: {type(valor)})")
        
        return db_taller
        
    except IntegrityError as e:
        print(f"Error de integridad en la BD: {e}")
        print(f"Detalles del error: {e.orig}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error de integridad: {str(e.orig)}"
        )
    
    except Exception as e:
        print(f"Error inesperado al crear taller: {e}")
        print(f"Tipo de error: {type(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/", response_model=List[schemas.TallerOut])
def listar_talleres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    print(f"=== LISTANDO TALLERES ===")
    print(f"Parámetros: skip={skip}, limit={limit}")
    
    try:
        talleres = db.query(models.ProduccionTaller).offset(skip).limit(limit).all()
        print(f"Talleres encontrados: {len(talleres)}")
        
        # Log de cada taller encontrado
        for i, taller in enumerate(talleres):
            print(f"Taller {i+1}: ID={taller.id}, Codigo={taller.codigo}, Nombre={taller.nombre}")
        
        return talleres
        
    except Exception as e:
        print(f"Error al listar talleres: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener talleres: {str(e)}"
        )

@router.get("/{id_taller}", response_model=schemas.TallerOut)
def obtener_taller(id_taller: int, db: Session = Depends(get_db)):
    print(f"=== OBTENIENDO TALLER ID: {id_taller} ===")
    
    try:
        taller = db.query(models.ProduccionTaller).filter(
            models.ProduccionTaller.id == id_taller
        ).first()
        
        if not taller:
            print(f"Taller con ID {id_taller} no encontrado")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Taller no encontrado"
            )
        
        print(f"Taller encontrado: {taller.codigo} - {taller.nombre}")
        return taller
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al obtener taller {id_taller}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener taller: {str(e)}"
        )

@router.put("/{id_taller}", response_model=schemas.TallerOut)
def actualizar_taller(
    id_taller: int, 
    datos: schemas.TallerUpdate, 
    db: Session = Depends(get_db)
):
    print(f"=== ACTUALIZANDO TALLER ID: {id_taller} ===")
    
    try:
        # Log de datos recibidos
        datos_actualizacion = datos.model_dump(exclude_unset=True)
        print(f"Datos de actualización: {json.dumps(datos_actualizacion, indent=2, default=str)}")
        
        taller = db.query(models.ProduccionTaller).filter(
            models.ProduccionTaller.id == id_taller
        ).first()
        
        if not taller:
            print(f"Taller con ID {id_taller} no encontrado para actualizar")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Taller no encontrado"
            )
        
        print(f"Taller encontrado: {taller.codigo} - {taller.nombre}")
        
        # Aplicar actualizaciones
        print("Aplicando actualizaciones:")
        for campo, valor in datos_actualizacion.items():
            valor_anterior = getattr(taller, campo, None)
            setattr(taller, campo, valor)
            print(f"  {campo}: {valor_anterior} -> {valor}")
        
        db.commit()
        db.refresh(taller)
        
        print(f"Taller actualizado exitosamente")
        return taller
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al actualizar taller {id_taller}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar taller: {str(e)}"
        )

@router.delete("/{id_taller}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_taller(id_taller: int, db: Session = Depends(get_db)):
    print(f"=== BORRANDO TALLER ID: {id_taller} ===")
    
    try:
        taller = db.query(models.ProduccionTaller).filter(
            models.ProduccionTaller.id == id_taller
        ).first()
        
        if not taller:
            print(f"Taller con ID {id_taller} no encontrado para borrar")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Taller no encontrado"
            )
        
        print(f"Taller encontrado para borrar: {taller.codigo} - {taller.nombre}")
        
        db.delete(taller)
        db.commit()
        
        print(f"Taller borrado exitosamente")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al borrar taller {id_taller}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al borrar taller: {str(e)}"
        )