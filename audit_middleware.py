# audit_middleware.py
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import json
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AuditMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        # Solo auditar rutas que requieren autenticación
        # Excluir rutas públicas como /docs, /health, etc.
        excluded_paths = ["/docs", "/redoc", "/openapi.json", "/health", "/"]
        
        if any(request.url.path.startswith(path) for path in excluded_paths):
            return await call_next(request)
        
        # Capturar datos de la petición
        start_time = datetime.now()
        api_key = None
        request_body = None
        
        try:
            # Obtener API Key del header
            api_key = request.headers.get("X-API-Key")
            
            # Leer el body de la petición si existe
            if request.method in ["POST", "PUT", "PATCH"]:
                body = await request.body()
                if body:
                    try:
                        request_body = json.loads(body.decode("utf-8"))
                    except json.JSONDecodeError:
                        request_body = {"raw_body": body.decode("utf-8", errors="ignore")}
                
                # Recrear el request para que el body esté disponible para los endpoints
                async def receive():
                    return {"type": "http.request", "body": body}
                
                request._receive = receive
        
        except Exception as e:
            logger.error(f"Error capturing request data: {e}")
        
        # Procesar la petición
        response = await call_next(request)
        
        # Solo registrar si la autenticación fue exitosa (status < 400)
        if response.status_code < 400 and api_key:
            try:
                await self._log_request(
                    endpoint=str(request.url.path),
                    method=request.method,
                    api_key=api_key,
                    request_body=request_body,
                    query_params=dict(request.query_params),
                    user_agent=request.headers.get("user-agent"),
                    ip_address=request.client.host if request.client else None,
                    status_code=response.status_code,
                    timestamp=start_time
                )
            except Exception as e:
                logger.error(f"Error logging request: {e}")
        
        return response
    
    async def _log_request(
        self,
        endpoint: str,
        method: str,
        api_key: str,
        request_body: Dict[Any, Any],
        query_params: Dict[str, str],
        user_agent: str,
        ip_address: str,
        status_code: int,
        timestamp: datetime
    ):
        """Guardar el log de la petición en la base de datos"""
        db = SessionLocal()
        try:
            audit_log = models.AuditLog(
                endpoint=endpoint,
                method=method,
                api_key=api_key,
                request_body=json.dumps(request_body) if request_body else None,
                query_params=json.dumps(query_params) if query_params else None,
                user_agent=user_agent,
                ip_address=ip_address,
                status_code=status_code,
                timestamp=timestamp
            )
            
            db.add(audit_log)
            db.commit()
            
        except Exception as e:
            logger.error(f"Failed to save audit log: {e}")
            db.rollback()
        finally:
            db.close()