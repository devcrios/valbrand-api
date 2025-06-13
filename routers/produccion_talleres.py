from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from dependencies import get_db, get_api_key
import models, schemas
import logging
import json

# Configurar logger
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/produccion/talleres",
    tags=["produccion", "talleres"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/", response_model=schemas.TallerOut, status_code=status.HTTP_201_CREATED)
def crear_taller(taller: schemas.TallerCreate, db: Session = Depends(get_db)):
    logger.info(f"=== CREANDO NUEVO TALLER ===")
    
    # Log de datos recibidos
    try:
        datos_recibidos = taller.model_dump()
        logger.info(f"Datos recibidos: {json.dumps(datos_recibidos, indent=2, default=str)}")
    except Exception as e:
        logger.error(f"Error al serializar datos recibidos: {e}")
        logger.info(f"Datos recibidos (raw): {taller}")
    
    # Log de validación del schema
    logger.info(f"Tipo de schema recibido: {type(taller)}")
    logger.info(f"Campos del schema: {list(taller.model_fields.keys()) if hasattr(taller, 'model_fields') else 'No disponible'}")
    
    try:
        # Crear el objeto de base de datos
        logger.info("Creando objeto ProduccionTaller...")
        db_taller = models.ProduccionTaller(**taller.model_dump())
        logger.info(f"Objeto creado exitosamente: {type(db_taller)}")
        
        # Log de los datos que se van a insertar
        logger.info("Datos a insertar en la BD:")
        for campo, valor in taller.model_dump().items():
            logger.info(f"  {campo}: {valor} (tipo: {type(valor)})")
        
        # Intentar guardar en la base de datos
        logger.info("Agregando objeto a la sesión de BD...")
        db.add(db_taller)
        
        logger.info("Ejecutando commit...")
        db.commit()
        
        logger.info("Ejecutando refresh...")
        db.refresh(db_taller)
        
        logger.info(f"Taller creado exitosamente con ID: {db_taller.id}")
        
        # Log del objeto retornado
        logger.info("Datos del taller creado:")
        for column in db_taller.__table__.columns:
            valor = getattr(db_taller, column.name)
            logger.info(f"  {column.name}: {valor} (tipo: {type(valor)})")
        
        return db_taller
        
    except IntegrityError as e:
        logger.error(f"Error de integridad en la BD: {e}")
        logger.error(f"Detalles del error: {e.orig}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error de integridad: {str(e.orig)}"
        )
    
    except Exception as e:
        logger.error(f"Error inesperado al crear taller: {e}")
        logger.error(f"Tipo de error: {type(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/", response_model=List[schemas.TallerOut])
def listar_talleres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"=== LISTANDO TALLERES ===")
    logger.info(f"Parámetros: skip={skip}, limit={limit}")
    
    try:
        talleres = db.query(models.ProduccionTaller).offset(skip).limit(limit).all()
        logger.info(f"Talleres encontrados: {len(talleres)}")
        
        # Log de cada taller encontrado
        for i, taller in enumerate(talleres):
            logger.info(f"Taller {i+1}: ID={taller.id}, Codigo={taller.codigo}, Nombre={taller.nombre}")
        
        return talleres
        
    except Exception as e:
        logger.error(f"Error al listar talleres: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener talleres: {str(e)}"
        )

@router.get("/{id_taller}", response_model=schemas.TallerOut)
def obtener_taller(id_taller: int, db: Session = Depends(get_db)):
    logger.info(f"=== OBTENIENDO TALLER ID: {id_taller} ===")
    
    try:
        taller = db.query(models.ProduccionTaller).filter(
            models.ProduccionTaller.id == id_taller
        ).first()
        
        if not taller:
            logger.warning(f"Taller con ID {id_taller} no encontrado")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Taller no encontrado"
            )
        
        logger.info(f"Taller encontrado: {taller.codigo} - {taller.nombre}")
        return taller
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener taller {id_taller}: {e}")
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
    logger.info(f"=== ACTUALIZANDO TALLER ID: {id_taller} ===")
    
    try:
        # Log de datos recibidos
        datos_actualizacion = datos.model_dump(exclude_unset=True)
        logger.info(f"Datos de actualización: {json.dumps(datos_actualizacion, indent=2, default=str)}")
        
        taller = db.query(models.ProduccionTaller).filter(
            models.ProduccionTaller.id == id_taller
        ).first()
        
        if not taller:
            logger.warning(f"Taller con ID {id_taller} no encontrado para actualizar")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Taller no encontrado"
            )
        
        logger.info(f"Taller encontrado: {taller.codigo} - {taller.nombre}")
        
        # Aplicar actualizaciones
        logger.info("Aplicando actualizaciones:")
        for campo, valor in datos_actualizacion.items():
            valor_anterior = getattr(taller, campo, None)
            setattr(taller, campo, valor)
            logger.info(f"  {campo}: {valor_anterior} -> {valor}")
        
        db.commit()
        db.refresh(taller)
        
        logger.info(f"Taller actualizado exitosamente")
        return taller
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar taller {id_taller}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar taller: {str(e)}"
        )

@router.delete("/{id_taller}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_taller(id_taller: int, db: Session = Depends(get_db)):
    logger.info(f"=== BORRANDO TALLER ID: {id_taller} ===")
    
    try:
        taller = db.query(models.ProduccionTaller).filter(
            models.ProduccionTaller.id == id_taller
        ).first()
        
        if not taller:
            logger.warning(f"Taller con ID {id_taller} no encontrado para borrar")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Taller no encontrado"
            )
        
        logger.info(f"Taller encontrado para borrar: {taller.codigo} - {taller.nombre}")
        
        db.delete(taller)
        db.commit()
        
        logger.info(f"Taller borrado exitosamente")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al borrar taller {id_taller}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al borrar taller: {str(e)}"
        )