from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import logging

# Importar el middleware de auditoría
from audit_middleware import AuditMiddleware

from routers.clients import router as clients_router
from routers.users import router as users_router
from routers.project_types import router as tipos_router
from routers.projects import router as projects_router
from routers.moldes import router as moldes_router
from routers.archivos_moldes import router as archivos_router
from routers.muestras import router as muestras_router
from routers.imagenes_muestras import router as imagenes_router
from routers.produccion_talleres import router as talleres_router
from routers.produccion_etapas import router as etapas_router
from routers.produccion_planes import router as planes_router
from routers.produccion_detalle_plan import router as detalle_router
from routers.produccion_materiales import router as materiales_router
from routers.produccion_materiales_proyecto import router as matproy_router
from routers.branding_proyectos import router as branding_proyectos_router
from routers.branding_entregables import router as branding_entregables_router
from routers.branding_revisiones import router as branding_revisiones_router
from routers.branding_feedback import router as branding_feedback_router
from routers.financiero_facturas import router as facturas_router
from routers.financiero_pagos import router as pagos_router
from routers.financiero_gastos import router as gastos_router
from routers.financiero_cuentas_cobrar import router as cuentas_router
from routers import (
    ecommerce_proyectos,
    ecommerce_credenciales,
    ecommerce_documentos,
    ecommerce_datos_marca
)
from routers.auth_routes import router as auth_router
from routers.audit_router import router as audit_router  # Importar el router de auditoría

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ValBrand CRM",
    description="API del CRM de ValBrand",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ORDEN CORRECTO DE MIDDLEWARES
# El orden importa: se ejecutan en orden inverso al registro

# 1. Primero agregar middleware de auditoría (se ejecutará último, después de procesar la respuesta)
app.add_middleware(AuditMiddleware)

# 2. Después CORS (se ejecutará antes que auditoría, pero después de procesar la request)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción especifica dominios específicos
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Core routers
app.include_router(clients_router)
app.include_router(users_router)

# Project routers
app.include_router(tipos_router)
app.include_router(projects_router)

# Molding routers
app.include_router(moldes_router)
app.include_router(archivos_router)
app.include_router(muestras_router)
app.include_router(imagenes_router)

# Production routers
app.include_router(talleres_router)
app.include_router(etapas_router)
app.include_router(planes_router)
app.include_router(detalle_router)
app.include_router(materiales_router)
app.include_router(matproy_router)

# Branding routers
app.include_router(branding_proyectos_router)
app.include_router(branding_entregables_router)
app.include_router(branding_revisiones_router)
app.include_router(branding_feedback_router)

# E-commerce routers
app.include_router(ecommerce_proyectos.router)
app.include_router(ecommerce_credenciales.router)
app.include_router(ecommerce_documentos.router)
app.include_router(ecommerce_datos_marca.router)

# Financial routers
app.include_router(facturas_router)
app.include_router(pagos_router)
app.include_router(gastos_router)
app.include_router(cuentas_router)

# Authentication router
app.include_router(auth_router)

# Audit router (agregar el router de auditoría)
app.include_router(audit_router)


@app.get("/", tags=["root"])
def read_root():
    """Endpoint raíz de la API"""
    return {
        "message": "Bienvenido a ValBrand CRM API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["health"])
def health_check():
    """Endpoint de verificación de salud del sistema"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "ValBrand CRM API"
    }

# Endpoint de prueba para verificar auditoría
@app.post("/test/audit", tags=["test"])
def test_audit_endpoint():
    """Endpoint de prueba para verificar que la auditoría funciona"""
    return {
        "message": "Este endpoint debería aparecer en los logs de auditoría",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )