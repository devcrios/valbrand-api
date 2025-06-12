# audit_router.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
import models
from dependencies import get_db, get_api_key
from pydantic import BaseModel

router = APIRouter(
    prefix="/audit",
    tags=["audit"],
    dependencies=[Depends(get_api_key)]
)

class AuditLogResponse(BaseModel):
    id: int
    endpoint: str
    method: str
    api_key: str
    request_body: Optional[str]
    query_params: Optional[str]
    user_agent: Optional[str]
    ip_address: Optional[str]
    status_code: Optional[int]
    timestamp: datetime
    
    class Config:
        from_attributes = True

class AuditStats(BaseModel):
    total_requests: int
    unique_endpoints: int
    methods_count: Dict[str, int]
    status_codes_count: Dict[str, int]
    requests_by_day: List[Dict[str, Any]]

@router.get("/logs", response_model=List[AuditLogResponse])
def get_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    endpoint: Optional[str] = Query(None, description="Filtrar por endpoint"),
    method: Optional[str] = Query(None, description="Filtrar por método HTTP"),
    api_key: Optional[str] = Query(None, description="Filtrar por API key"),
    date_from: Optional[date] = Query(None, description="Fecha desde (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="Fecha hasta (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Obtener logs de auditoría con filtros opcionales"""
    
    query = db.query(models.AuditLog)
    
    # Aplicar filtros
    if endpoint:
        query = query.filter(models.AuditLog.endpoint.ilike(f"%{endpoint}%"))
    
    if method:
        query = query.filter(models.AuditLog.method == method.upper())
    
    if api_key:
        query = query.filter(models.AuditLog.api_key == api_key)
    
    if date_from:
        query = query.filter(models.AuditLog.timestamp >= date_from)
    
    if date_to:
        # Agregar 1 día para incluir todo el día
        date_to_end = datetime.combine(date_to, datetime.max.time())
        query = query.filter(models.AuditLog.timestamp <= date_to_end)
    
    # Ordenar por timestamp descendente
    query = query.order_by(desc(models.AuditLog.timestamp))
    
    return query.offset(skip).limit(limit).all()

@router.get("/logs/{log_id}", response_model=AuditLogResponse)
def get_audit_log(log_id: int, db: Session = Depends(get_db)):
    """Obtener un log específico por ID"""
    
    log = db.query(models.AuditLog).filter(models.AuditLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    
    return log

@router.get("/stats", response_model=AuditStats)
def get_audit_stats(
    date_from: Optional[date] = Query(None, description="Fecha desde (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="Fecha hasta (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de los logs de auditoría"""
    
    query = db.query(models.AuditLog)
    
    # Aplicar filtros de fecha
    if date_from:
        query = query.filter(models.AuditLog.timestamp >= date_from)
    
    if date_to:
        date_to_end = datetime.combine(date_to, datetime.max.time())
        query = query.filter(models.AuditLog.timestamp <= date_to_end)
    
    # Obtener estadísticas básicas
    total_requests = query.count()
    
    # Endpoints únicos
    unique_endpoints = query.distinct(models.AuditLog.endpoint).count()
    
    # Conteo por método
    methods_query = db.query(
        models.AuditLog.method,
        db.func.count(models.AuditLog.id).label('count')
    )
    if date_from:
        methods_query = methods_query.filter(models.AuditLog.timestamp >= date_from)
    if date_to:
        methods_query = methods_query.filter(models.AuditLog.timestamp <= date_to_end)
    
    methods_count = {
        method: count for method, count in 
        methods_query.group_by(models.AuditLog.method).all()
    }
    
    # Conteo por código de estado
    status_query = db.query(
        models.AuditLog.status_code,
        db.func.count(models.AuditLog.id).label('count')
    )
    if date_from:
        status_query = status_query.filter(models.AuditLog.timestamp >= date_from)
    if date_to:
        status_query = status_query.filter(models.AuditLog.timestamp <= date_to_end)
    
    status_codes_count = {
        str(status): count for status, count in 
        status_query.group_by(models.AuditLog.status_code).all()
        if status is not None
    }
    
    # Requests por día (últimos 7 días)
    requests_by_day_query = db.query(
        db.func.date(models.AuditLog.timestamp).label('date'),
        db.func.count(models.AuditLog.id).label('count')
    )
    if date_from:
        requests_by_day_query = requests_by_day_query.filter(models.AuditLog.timestamp >= date_from)
    if date_to:
        requests_by_day_query = requests_by_day_query.filter(models.AuditLog.timestamp <= date_to_end)
    
    requests_by_day = [
        {"date": str(date_val), "count": count}
        for date_val, count in requests_by_day_query.group_by(
            db.func.date(models.AuditLog.timestamp)
        ).order_by(db.func.date(models.AuditLog.timestamp)).all()
    ]
    
    return AuditStats(
        total_requests=total_requests,
        unique_endpoints=unique_endpoints,
        methods_count=methods_count,
        status_codes_count=status_codes_count,
        requests_by_day=requests_by_day
    )

@router.delete("/logs/cleanup")
def cleanup_old_logs(
    days_to_keep: int = Query(30, ge=1, le=365, description="Días de logs a mantener"),
    db: Session = Depends(get_db)
):
    """Limpiar logs antiguos"""
    
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    
    deleted_count = db.query(models.AuditLog).filter(
        models.AuditLog.timestamp < cutoff_date
    ).delete()
    
    db.commit()
    
    return {
        "message": f"Se eliminaron {deleted_count} logs anteriores a {cutoff_date.date()}",
        "deleted_count": deleted_count
    }