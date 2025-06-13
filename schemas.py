from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import date, datetime
from models import ClienteEstado, ClienteTipo, UsuarioEstado, MoldeEstado
from models import EcommerceProyectoEstado, EcommercePlataforma

class ClienteBase(BaseModel):
    nombre: str
    nombre_contacto: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = None
    codigo_postal: Optional[str] = None
    rfc: Optional[str] = None
    estado: ClienteEstado = ClienteEstado.ACTIVO
    notas: Optional[str] = None
    tipo_cliente: ClienteTipo
    creado_por: Optional[int] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    nombre_contacto: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = None
    codigo_postal: Optional[str] = None
    rfc: Optional[str] = None
    estado: Optional[ClienteEstado] = None
    notas: Optional[str] = None
    tipo_cliente: Optional[ClienteTipo] = None
    creado_por: Optional[int] = None

class Cliente(ClienteBase):
    id_cliente: int
    fecha_registro: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True

class UsuarioBase(BaseModel):
    nombre: str
    apellidos: Optional[str]
    email: EmailStr
    id_rol: int
    telefono: Optional[str]
    cargo: Optional[str]
    departamento: Optional[str]
    estado: UsuarioEstado = UsuarioEstado.ACTIVO
    configuracion_notificaciones: Optional[Dict]
    creado_por: Optional[int]

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[EmailStr] = None
    id_rol: Optional[int] = None
    telefono: Optional[str] = None
    cargo: Optional[str] = None
    departamento: Optional[str] = None
    estado: Optional[UsuarioEstado] = None
    password: Optional[str] = None
    configuracion_notificaciones: Optional[Dict] = None
    creado_por: Optional[int] = None

class Usuario(UsuarioBase):
    id_usuario: int
    fecha_registro: datetime
    fecha_ultimo_acceso: Optional[datetime]

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserInfo(BaseModel):
    id_usuario: int
    nombre: str
    apellidos: Optional[str]
    email: str
    cargo: Optional[str]
    departamento: Optional[str]
    id_rol: int

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserInfo

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class MessageResponse(BaseModel):
    message: str

class LoginAttempt(BaseModel):
    email: str
    success: bool
    timestamp: datetime
    ip_address: Optional[str] = None

class ProyectoTipoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: Optional[bool] = True

class ProyectoTipoCreate(ProyectoTipoBase):
    pass

class ProyectoTipoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

class ProyectoTipoOut(ProyectoTipoBase):
    id_tipo_proyecto: int
    
    class Config:
        from_attributes = True

class ProyectoBase(BaseModel):
    codigo_proyecto: str = Field(..., max_length=50)
    id_cliente: int
    nombre_proyecto: str
    id_tipo_proyecto: int
    descripcion: Optional[str] = None
    especificaciones_tecnicas: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_entrega_estimada: Optional[date] = None
    estado: Optional[str] = None
    prioridad: Optional[str] = None
    notas: Optional[str] = None
    creado_por: Optional[int] = None

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoUpdate(BaseModel):
    codigo_proyecto: Optional[str] = None
    id_cliente: Optional[int] = None
    nombre_proyecto: Optional[str] = None
    id_tipo_proyecto: Optional[int] = None
    descripcion: Optional[str] = None
    especificaciones_tecnicas: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_entrega_estimada: Optional[date] = None
    estado: Optional[str] = None
    prioridad: Optional[str] = None
    progreso_porcentaje: Optional[float] = None
    notas: Optional[str] = None
    creado_por: Optional[int] = None

class ProyectoOut(ProyectoBase):
    id_proyecto: int
    fecha_entrega_real: Optional[date] = None
    fecha_finalizacion: Optional[date] = None
    progreso_porcentaje: float = 0.0
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    class Config:
        from_attributes = True

class MoldeBase(BaseModel):
    codigo_molde: str
    id_proyecto: int
    nombre_molde: str
    categoria: Optional[str]
    talla: Optional[str]
    version: Optional[str]
    estado: Optional[MoldeEstado] 
    notas: Optional[str]
    medidas: Optional[str]
    observaciones_tecnicas: Optional[str]
    creado_por: Optional[int]

class MoldeCreate(MoldeBase): 
    pass

class MoldeUpdate(BaseModel):
    codigo_molde: Optional[str] = None
    id_proyecto: Optional[int] = None
    nombre_molde: Optional[str] = None
    categoria: Optional[str] = None
    talla: Optional[str] = None
    version: Optional[str] = None
    estado: Optional[str] = None
    notas: Optional[str] = None
    medidas: Optional[str] = None
    observaciones_tecnicas: Optional[str] = None
    creado_por: Optional[int] = None

class MoldeOut(MoldeBase):
    id_molde: int
    fecha_creacion: datetime
    fecha_modificacion: datetime
    class Config: 
        from_attributes = True

class ArchivoMoldeBase(BaseModel):
    id_molde: int
    nombre_archivo: str
    tipo_archivo: str
    version: Optional[str]
    es_principal: Optional[bool]
    notas: Optional[str]
    subido_por: Optional[int]

class ArchivoMoldeCreate(ArchivoMoldeBase): 
    archivo: bytes

class ArchivoMoldeUpdate(BaseModel):
    id_molde: Optional[int] = None
    nombre_archivo: Optional[str] = None
    tipo_archivo: Optional[str] = None
    version: Optional[str] = None
    es_principal: Optional[bool] = None
    notas: Optional[str] = None
    subido_por: Optional[int] = None

class ArchivoMoldeOut(ArchivoMoldeBase):
    id_archivo: int
    fecha_subida: datetime
    class Config: 
        from_attributes = True

class MuestraBase(BaseModel):
    codigo_muestra: str
    id_proyecto: int
    id_molde: Optional[int]
    nombre_muestra: str
    descripcion: Optional[str]
    talla: Optional[str]
    color: Optional[str]
    material: Optional[str]
    estado: Optional[str]
    feedback_cliente: Optional[str]
    feedback_interno: Optional[str]
    costo: Optional[float]
    creada_por: Optional[int]

class MuestraCreate(MuestraBase): 
    pass

class MuestraUpdate(BaseModel):
    codigo_muestra: Optional[str] = None
    id_proyecto: Optional[int] = None
    id_molde: Optional[int] = None
    nombre_muestra: Optional[str] = None
    descripcion: Optional[str] = None
    talla: Optional[str] = None
    color: Optional[str] = None
    material: Optional[str] = None
    estado: Optional[str] = None
    feedback_cliente: Optional[str] = None
    feedback_interno: Optional[str] = None
    costo: Optional[float] = None
    creada_por: Optional[int] = None

class MuestraOut(MuestraBase):
    id_muestra: int
    fecha_creacion: datetime
    fecha_entrega_estimada: Optional[datetime]
    fecha_entrega_real: Optional[datetime]
    class Config: 
        from_attributes = True

class ImagenMuestraBase(BaseModel):
    id_muestra: int
    nombre_imagen: Optional[str]
    descripcion: Optional[str]
    es_principal: Optional[bool]
    orden_visualizacion: Optional[int]
    subido_por: Optional[int]

class ImagenMuestraCreate(ImagenMuestraBase): 
    imagen: bytes

class ImagenMuestraUpdate(BaseModel):
    id_muestra: Optional[int] = None
    nombre_imagen: Optional[str] = None
    descripcion: Optional[str] = None
    es_principal: Optional[bool] = None
    orden_visualizacion: Optional[int] = None
    subido_por: Optional[int] = None

class ImagenMuestraOut(ImagenMuestraBase):
    id_imagen: int
    fecha_subida: datetime
    class Config: 
        from_attributes = True

class TallerBase(BaseModel):
    nombre: str
    codigo: Optional[str]
    direccion: Optional[str]
    contacto: Optional[str]
    telefono: Optional[str]
    email: Optional[str]
    especialidad: Optional[str]
    capacidad: Optional[int]
    estado: Optional[str]
    calificacion: Optional[float]
    notas: Optional[str]

class TallerCreate(TallerBase): 
    pass

class TallerUpdate(BaseModel):
    nombre: Optional[str] = None
    codigo: Optional[str] = None
    direccion: Optional[str] = None
    contacto: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    especialidad: Optional[str] = None
    capacidad: Optional[int] = None
    estado: Optional[str] = None
    calificacion: Optional[float] = None
    notas: Optional[str] = None

class TallerOut(TallerBase):
    id_taller: int
    fecha_reg: datetime
    class Config: 
        from_attributes = True

class EtapaBase(BaseModel):
    nombre: str
    descripcion: Optional[str]
    orden: Optional[int]
    tiempo_estim: Optional[float]
    activo: Optional[bool]

class EtapaCreate(EtapaBase): 
    pass

class EtapaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    orden: Optional[int] = None
    tiempo_estim: Optional[float] = None
    activo: Optional[bool] = None

class EtapaOut(EtapaBase):
    id_etapa: int
    class Config: 
        from_attributes = True

class PlanBase(BaseModel):
    codigo_plan: str
    id_proyecto: int
    id_taller: Optional[int]
    fecha_ini_est: Optional[date]
    fecha_fin_est: Optional[date]
    estado: Optional[str]
    cantidad_prod: int
    prioridad: Optional[str]
    notas: Optional[str]
    costo_est: Optional[float]
    responsable: Optional[str]
    creado_por: Optional[int]

class PlanCreate(PlanBase): 
    pass

class PlanUpdate(BaseModel):
    codigo_plan: Optional[str] = None
    id_proyecto: Optional[int] = None
    id_taller: Optional[int] = None
    fecha_ini_est: Optional[date] = None
    fecha_fin_est: Optional[date] = None
    estado: Optional[str] = None
    cantidad_prod: Optional[int] = None
    cantidad_comp: Optional[int] = None
    prioridad: Optional[str] = None
    notas: Optional[str] = None
    costo_est: Optional[float] = None
    costo_real: Optional[float] = None
    responsable: Optional[str] = None
    creado_por: Optional[int] = None

class PlanOut(PlanBase):
    id_plan: int
    cantidad_comp: int
    fecha_ini_real: Optional[date]
    fecha_fin_real: Optional[date]
    fecha_creacion: datetime
    class Config: 
        from_attributes = True

class DetallePlanBase(BaseModel):
    id_plan: int
    id_etapa: int
    fecha_ini_est: Optional[date]
    fecha_fin_est: Optional[date]
    estado: Optional[str]
    responsable: Optional[str]
    observaciones: Optional[str]
    tiempo_inv: Optional[float]
    pct_completado: Optional[float]

class DetallePlanCreate(DetallePlanBase): 
    pass

class DetallePlanUpdate(BaseModel):
    id_plan: Optional[int] = None
    id_etapa: Optional[int] = None
    fecha_ini_est: Optional[date] = None
    fecha_fin_est: Optional[date] = None
    estado: Optional[str] = None
    responsable: Optional[str] = None
    observaciones: Optional[str] = None
    tiempo_inv: Optional[float] = None
    pct_completado: Optional[float] = None

class DetallePlanOut(DetallePlanBase):
    id_detalle: int
    class Config: 
        from_attributes = True

class MaterialBase(BaseModel):
    codigo_material: str
    nombre: str
    descripcion: Optional[str]
    categoria: Optional[str]
    unidad_medida: Optional[str]
    stock_actual: Optional[float]
    stock_minimo: Optional[float]
    costo_unitario: Optional[float]
    proveedor: Optional[str]
    estado: Optional[str]

class MaterialCreate(MaterialBase): 
    pass

class MaterialUpdate(BaseModel):
    codigo_material: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    unidad_medida: Optional[str] = None
    stock_actual: Optional[float] = None
    stock_minimo: Optional[float] = None
    costo_unitario: Optional[float] = None
    proveedor: Optional[str] = None
    estado: Optional[str] = None

class MaterialOut(MaterialBase):
    id_material: int
    fecha_registro: datetime
    class Config: 
        from_attributes = True

class MatProyectoBase(BaseModel):
    id_proyecto: int
    id_material: int
    cantidad_req: float
    notas: Optional[str]

class MatProyectoCreate(MatProyectoBase):
    costo_unit: Optional[float]

class MatProyectoUpdate(BaseModel):
    id_proyecto: Optional[int] = None
    id_material: Optional[int] = None
    cantidad_req: Optional[float] = None
    cantidad_uso: Optional[float] = None
    costo_unit: Optional[float] = None
    costo_total: Optional[float] = None
    notas: Optional[str] = None

class MatProyectoOut(MatProyectoBase):
    id_mat_proy: int
    cantidad_uso: Optional[float]
    costo_total: Optional[float]
    fecha_asig: date
    class Config: 
        from_attributes = True

# Branding proyectos
class BrandingProyectoBase(BaseModel):
    id_proyecto: int
    tipo_servicio: str
    brief_cliente: Optional[str]
    objetivos: Optional[str]
    publico_objetivo: Optional[str]
    competencia: Optional[str]
    referencias_visuales: Optional[str]
    fecha_inicio: Optional[date]
    fecha_entrega_estimada: Optional[date]
    fecha_entrega_real: Optional[date]
    estado: Optional[str]
    numero_revisiones: Optional[int]
    revisiones_incluidas: Optional[int]
    feedback_cliente: Optional[str]
    notas_internas: Optional[str]
    responsable_diseno: Optional[str]

class BrandingProyectoCreate(BrandingProyectoBase):
    pass

class BrandingProyectoUpdate(BaseModel):
    id_proyecto: Optional[int] = None
    tipo_servicio: Optional[str] = None
    brief_cliente: Optional[str] = None
    objetivos: Optional[str] = None
    publico_objetivo: Optional[str] = None
    competencia: Optional[str] = None
    referencias_visuales: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_entrega_estimada: Optional[date] = None
    fecha_entrega_real: Optional[date] = None
    estado: Optional[str] = None
    numero_revisiones: Optional[int] = None
    revisiones_incluidas: Optional[int] = None
    feedback_cliente: Optional[str] = None
    notas_internas: Optional[str] = None
    responsable_diseno: Optional[str] = None

class BrandingProyectoOut(BrandingProyectoBase):
    id_proyecto_branding: int
    class Config:
        from_attributes = True

# Branding entregables
class EntregableBase(BaseModel):
    id_proyecto_branding: int
    nombre_entregable: str
    tipo_entregable: str
    descripcion: Optional[str]
    nombre_archivo: Optional[str]
    extension: Optional[str]
    tamano_archivo: Optional[int]
    version: Optional[str]
    estado: Optional[str]
    creado_por: Optional[int]

class EntregableCreate(EntregableBase):
    archivo: bytes

class EntregableUpdate(BaseModel):
    id_proyecto_branding: Optional[int] = None
    nombre_entregable: Optional[str] = None
    tipo_entregable: Optional[str] = None
    descripcion: Optional[str] = None
    nombre_archivo: Optional[str] = None
    extension: Optional[str] = None
    tamano_archivo: Optional[int] = None
    version: Optional[str] = None
    estado: Optional[str] = None
    creado_por: Optional[int] = None

class EntregableOut(EntregableBase):
    id_entregable: int
    fecha_creacion: datetime
    class Config:
        from_attributes = True

# Branding revisiones
class RevisionBase(BaseModel):
    id_proyecto_branding: int
    numero_revision: int
    tipo_revision: str
    comentarios: Optional[str]
    cambios_solicitados: Optional[str]
    estado: Optional[str]
    fecha_limite: Optional[date]
    revisor: Optional[str]

class RevisionCreate(RevisionBase):
    pass

class RevisionUpdate(BaseModel):
    id_proyecto_branding: Optional[int] = None
    numero_revision: Optional[int] = None
    tipo_revision: Optional[str] = None
    comentarios: Optional[str] = None
    cambios_solicitados: Optional[str] = None
    estado: Optional[str] = None
    fecha_limite: Optional[date] = None
    revisor: Optional[str] = None

class RevisionOut(RevisionBase):
    id_revision: int
    fecha_revision: datetime
    archivos_revision: Optional[bytes]
    nombre_archivos: Optional[str]
    class Config:
        from_attributes = True

# Branding feedback fechas
class FeedbackFechaBase(BaseModel):
    id_proyecto_branding: int
    fecha_feedback: date
    comentario: str
    prioridad: Optional[str]
    estado: Optional[str]
    creado_por: Optional[int]

class FeedbackFechaCreate(FeedbackFechaBase):
    pass

class FeedbackFechaUpdate(BaseModel):
    id_proyecto_branding: Optional[int] = None
    fecha_feedback: Optional[date] = None
    comentario: Optional[str] = None
    prioridad: Optional[str] = None
    estado: Optional[str] = None
    creado_por: Optional[int] = None

class FeedbackFechaOut(FeedbackFechaBase):
    id_feedback: int
    fecha_creacion: datetime
    class Config:
        from_attributes = True

# Proyecto Ecommerce
class EcommerceProyectoBase(BaseModel):
    id_proyecto: int
    nombre_tienda: str
    url_tienda: Optional[str] = None
    dominio_principal: Optional[str] = None
    plataforma: EcommercePlataforma
    plan_hosting: Optional[str] = None
    funcionalidades_requeridas: Optional[str] = None
    numero_productos_estimado: Optional[int] = None
    metodos_pago: Optional[str] = None
    metodos_envio: Optional[str] = None
    fecha_lanzamiento_estimada: Optional[date] = None
    fecha_lanzamiento_real: Optional[date] = None
    estado: Optional[EcommerceProyectoEstado] = EcommerceProyectoEstado.PLANIFICACION
    ssl_configurado: Optional[bool] = None
    analytics_configurado: Optional[bool] = None
    seo_configurado: Optional[bool] = None
    notas: Optional[str] = None
    responsable_desarrollo: Optional[str] = None

class EcommerceProyectoCreate(EcommerceProyectoBase):
    pass

class EcommerceProyectoUpdate(BaseModel):
    id_proyecto: Optional[int] = None
    nombre_tienda: Optional[str] = None
    url_tienda: Optional[str] = None
    dominio_principal: Optional[str] = None
    plataforma: Optional[EcommercePlataforma] = None
    plan_hosting: Optional[str] = None
    funcionalidades_requeridas: Optional[str] = None
    numero_productos_estimado: Optional[int] = None
    metodos_pago: Optional[str] = None
    metodos_envio: Optional[str] = None
    fecha_lanzamiento_estimada: Optional[date] = None
    fecha_lanzamiento_real: Optional[date] = None
    estado: Optional[EcommerceProyectoEstado] = None
    ssl_configurado: Optional[bool] = None
    analytics_configurado: Optional[bool] = None
    seo_configurado: Optional[bool] = None
    notas: Optional[str] = None
    responsable_desarrollo: Optional[str] = None

class EcommerceProyectoOut(EcommerceProyectoBase):
    id_proyecto_ecommerce: int
    class Config:
        from_attributes = True

# Credencial
class EcommerceCredencialBase(BaseModel):
    id_proyecto_ecommerce: int
    tipo_credencial: str
    servicio: Optional[str] = None
    usuario: Optional[str] = None
    contrasena: Optional[str] = None
    url_acceso: Optional[str] = None
    email_recuperacion: Optional[str] = None
    notas: Optional[str] = None
    fecha_expiracion: Optional[date] = None
    activo: Optional[bool] = True

class EcommerceCredencialCreate(EcommerceCredencialBase):
    pass

class EcommerceCredencialUpdate(BaseModel):
    id_proyecto_ecommerce: Optional[int] = None
    tipo_credencial: Optional[str] = None
    servicio: Optional[str] = None
    usuario: Optional[str] = None
    contrasena: Optional[str] = None
    url_acceso: Optional[str] = None
    email_recuperacion: Optional[str] = None
    notas: Optional[str] = None
    fecha_expiracion: Optional[date] = None
    activo: Optional[bool] = None

class EcommerceCredencialOut(EcommerceCredencialBase):
    id_credencial: int
    fecha_creacion: datetime
    class Config:
        from_attributes = True

# Documento
class EcommerceDocumentoBase(BaseModel):
    id_proyecto_ecommerce: int
    nombre_documento: str
    tipo_documento: str
    descripcion: Optional[str] = None
    version: Optional[str] = None
    es_publico: Optional[bool] = False
    subido_por: Optional[int] = None

class EcommerceDocumentoCreate(EcommerceDocumentoBase):
    pass

class EcommerceDocumentoUpdate(BaseModel):
    id_proyecto_ecommerce: Optional[int] = None
    nombre_documento: Optional[str] = None
    tipo_documento: Optional[str] = None
    descripcion: Optional[str] = None
    version: Optional[str] = None
    es_publico: Optional[bool] = None
    subido_por: Optional[int] = None

class EcommerceDocumentoOut(EcommerceDocumentoBase):
    id_documento: int
    nombre_archivo: str
    extension: str
    tamano_archivo: int
    fecha_subida: datetime
    class Config:
        from_attributes = True

# Datos Marca
class EcommerceDatosMarcaBase(BaseModel):
    id_proyecto_ecommerce: int
    email_marca: Optional[str] = None
    contrasena_email: Optional[str] = None
    servidor_smtp: Optional[str] = None
    puerto_smtp: Optional[int] = None
    configuracion_ssl: Optional[bool] = True
    notas_email: Optional[str] = None
    configurado_por: Optional[int] = None

class EcommerceDatosMarcaCreate(EcommerceDatosMarcaBase):
    pass

class EcommerceDatosMarcaUpdate(BaseModel):
    id_proyecto_ecommerce: Optional[int] = None
    email_marca: Optional[str] = None
    contrasena_email: Optional[str] = None
    servidor_smtp: Optional[str] = None
    puerto_smtp: Optional[int] = None
    configuracion_ssl: Optional[bool] = None
    notas_email: Optional[str] = None
    configurado_por: Optional[int] = None

class EcommerceDatosMarcaOut(EcommerceDatosMarcaBase):
    id_datos_marca: int
    fecha_configuracion: datetime
    class Config:
        from_attributes = True

# ——— FACTURAS ———
class FacturaBase(BaseModel):
    numero_factura: str
    id_proyecto: int
    serie: Optional[str] = None
    folio: Optional[int] = None
    fecha_emision: date
    fecha_vencimiento: Optional[date] = None
    fecha_pago: Optional[date] = None
    subtotal: float
    descuento: Optional[float] = 0
    impuestos: float
    total: float
    moneda: Optional[str] = "MXN"
    tipo_cambio: Optional[float] = 1.0
    estado: Optional[str] = "BORRADOR"
    metodo_pago: Optional[str] = None
    forma_pago: Optional[str] = None
    condiciones_pago: Optional[str] = None
    notas: Optional[str] = None
    uuid_sat: Optional[str] = None
    archivo_xml: Optional[bytes] = None
    archivo_pdf: Optional[bytes] = None
    nombre_archivo_pdf: Optional[str] = None
    creada_por: Optional[int] = None

class FacturaCreate(FacturaBase): 
    pass

class FacturaUpdate(BaseModel):
    numero_factura: Optional[str] = None
    id_proyecto: Optional[int] = None
    serie: Optional[str] = None
    folio: Optional[int] = None
    fecha_emision: Optional[date] = None
    fecha_vencimiento: Optional[date] = None
    fecha_pago: Optional[date] = None
    subtotal: Optional[float] = None
    descuento: Optional[float] = None
    impuestos: Optional[float] = None
    total: Optional[float] = None
    moneda: Optional[str] = None
    tipo_cambio: Optional[float] = None
    estado: Optional[str] = None
    metodo_pago: Optional[str] = None
    forma_pago: Optional[str] = None
    condiciones_pago: Optional[str] = None
    notas: Optional[str] = None
    uuid_sat: Optional[str] = None
    archivo_xml: Optional[bytes] = None
    archivo_pdf: Optional[bytes] = None
    nombre_archivo_pdf: Optional[str] = None
    creada_por: Optional[int] = None

class FacturaOut(FacturaBase):
    id_factura: int
    fecha_creacion: datetime
    class Config:
        from_attributes = True

# ——— PAGOS ———
class PagoBase(BaseModel):
    numero_pago: str
    id_factura: int
    monto: float
    fecha_pago: date
    metodo_pago: str
    forma_pago: Optional[str] = None
    referencia: Optional[str] = None
    banco: Optional[str] = None
    cuenta: Optional[str] = None
    comprobante: Optional[bytes] = None
    nombre_comprobante: Optional[str] = None
    notas: Optional[str] = None
    registrado_por: Optional[int] = None

class PagoCreate(PagoBase): 
    pass

class PagoUpdate(BaseModel):
    numero_pago: Optional[str] = None
    id_factura: Optional[int] = None
    monto: Optional[float] = None
    fecha_pago: Optional[date] = None
    metodo_pago: Optional[str] = None
    forma_pago: Optional[str] = None
    referencia: Optional[str] = None
    banco: Optional[str] = None
    cuenta: Optional[str] = None
    comprobante: Optional[bytes] = None
    nombre_comprobante: Optional[str] = None
    notas: Optional[str] = None
    registrado_por: Optional[int] = None

class PagoOut(PagoBase):
    id_pago: int
    fecha_registro: datetime
    class Config:
        from_attributes = True

# ——— GASTOS ———
class GastoBase(BaseModel):
    numero_gasto: str
    id_proyecto: Optional[int] = None
    concepto: str
    descripcion: Optional[str] = None
    monto: float
    moneda: Optional[str] = "MXN"
    fecha_gasto: date
    categoria: str
    proveedor: Optional[str] = None
    metodo_pago: Optional[str] = None
    deducible: Optional[bool] = True
    comprobante: Optional[bytes] = None
    nombre_comprobante: Optional[str] = None
    notas: Optional[str] = None
    registrado_por: Optional[int] = None

class GastoCreate(GastoBase): 
    pass

class GastoUpdate(BaseModel):
    numero_gasto: Optional[str] = None
    id_proyecto: Optional[int] = None
    concepto: Optional[str] = None
    descripcion: Optional[str] = None
    monto: Optional[float] = None
    moneda: Optional[str] = None
    fecha_gasto: Optional[date] = None
    categoria: Optional[str] = None
    proveedor: Optional[str] = None
    metodo_pago: Optional[str] = None
    deducible: Optional[bool] = None
    comprobante: Optional[bytes] = None
    nombre_comprobante: Optional[str] = None
    notas: Optional[str] = None
    registrado_por: Optional[int] = None

class GastoOut(GastoBase):
    id_gasto: int
    fecha_registro: datetime
    class Config:
        from_attributes = True

# ——— CUENTAS POR COBRAR ———
class CuentaCobrarBase(BaseModel):
    id_cliente: int
    id_factura: Optional[int] = None
    concepto: str
    monto: float
    saldo_pendiente: float
    fecha_vencimiento: date
    dias_vencido: Optional[int] = 0
    estado: Optional[str] = "VIGENTE"
    notas: Optional[str] = None

class CuentaCobrarCreate(CuentaCobrarBase): 
    pass

class CuentaCobrarUpdate(BaseModel):
    id_cliente: Optional[int] = None
    id_factura: Optional[int] = None
    concepto: Optional[str] = None
    monto: Optional[float] = None
    saldo_pendiente: Optional[float] = None
    fecha_vencimiento: Optional[date] = None
    dias_vencido: Optional[int] = None
    estado: Optional[str] = None
    notas: Optional[str] = None

class CuentaCobrarOut(CuentaCobrarBase):
    id_cuenta_cobrar: int
    class Config:
        from_attributes = True