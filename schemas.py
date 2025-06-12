from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import date, datetime
from models import ClienteEstado, ClienteTipo, UsuarioEstado
from models import EcommerceProyectoEstado, EcommercePlataforma

class ClienteBase(BaseModel):
    nombre: str
    nombre_contacto: Optional[str]
    email: Optional[EmailStr]
    telefono: Optional[str]
    direccion: Optional[str]
    ciudad: Optional[str]
    pais: Optional[str]
    codigo_postal: Optional[str]
    rfc: Optional[str]
    estado: ClienteEstado = ClienteEstado.ACTIVO
    notas: Optional[str]
    tipo_cliente: ClienteTipo
    creado_por: Optional[int]

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str]
    nombre_contacto: Optional[str]
    email: Optional[EmailStr]
    telefono: Optional[str]
    direccion: Optional[str]
    ciudad: Optional[str]
    pais: Optional[str]
    codigo_postal: Optional[str]
    rfc: Optional[str]
    estado: Optional[ClienteEstado]
    notas: Optional[str]
    tipo_cliente: Optional[ClienteTipo]
    creado_por: Optional[int]

class Cliente(ClienteBase):
    id_cliente: int
    fecha_registro: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True

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
    nombre: Optional[str]
    apellidos: Optional[str]
    email: Optional[EmailStr]
    id_rol: Optional[int]
    telefono: Optional[str]
    cargo: Optional[str]
    departamento: Optional[str]
    estado: Optional[UsuarioEstado]
    password: Optional[str]
    configuracion_notificaciones: Optional[Dict]
    creado_por: Optional[int]

class Usuario(UsuarioBase):
    id_usuario: int
    fecha_registro: datetime
    fecha_ultimo_acceso: Optional[datetime]

    class Config:
        orm_mode = True

class ProyectoTipoBase(BaseModel):
    nombre: str
    descripcion: Optional[str]
    activo: Optional[bool] = True

class ProyectoTipoCreate(ProyectoTipoBase):
    pass

class ProyectoTipoUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    activo: Optional[bool]

class ProyectoTipoOut(ProyectoTipoBase):
    id_tipo_proyecto: int
    class Config:
        orm_mode = True

class ProyectoBase(BaseModel):
    codigo_proyecto: str = Field(..., max_length=50)
    id_cliente: int
    nombre_proyecto: str
    id_tipo_proyecto: int
    descripcion: Optional[str]
    especificaciones_tecnicas: Optional[str]
    fecha_inicio: Optional[datetime.date]
    fecha_entrega_estimada: Optional[datetime.date]
    estado: Optional[str]
    prioridad: Optional[str]
    notas: Optional[str]
    creado_por: Optional[int]

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoUpdate(BaseModel):
    nombre_proyecto: Optional[str]
    descripcion: Optional[str]
    especificaciones_tecnicas: Optional[str]
    fecha_inicio: Optional[datetime.date]
    fecha_entrega_estimada: Optional[datetime.date]
    estado: Optional[str]
    prioridad: Optional[str]
    progreso_porcentaje: Optional[float]
    notas: Optional[str]

class ProyectoOut(ProyectoBase):
    id_proyecto: int
    fecha_entrega_real: Optional[datetime.date]
    fecha_finalizacion: Optional[datetime.date]
    progreso_porcentaje: float
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    class Config:
        orm_mode = True

class MoldeBase(BaseModel):
    codigo_molde: str
    id_proyecto: int
    nombre_molde: str
    categoria: Optional[str]
    talla: Optional[str]
    version: Optional[str]
    estado: Optional[str]
    notas: Optional[str]
    medidas: Optional[str]
    observaciones_tecnicas: Optional[str]
    creado_por: Optional[int]

class MoldeCreate(MoldeBase): pass
class MoldeUpdate(BaseModel):
    nombre_molde: Optional[str]
    categoria: Optional[str]
    talla: Optional[str]
    version: Optional[str]
    estado: Optional[str]
    notas: Optional[str]
    medidas: Optional[str]
    observaciones_tecnicas: Optional[str]

class MoldeOut(MoldeBase):
    id_molde: int
    fecha_creacion: datetime
    fecha_modificacion: datetime
    class Config: orm_mode = True

class ArchivoMoldeBase(BaseModel):
    id_molde: int
    nombre_archivo: str
    tipo_archivo: str
    version: Optional[str]
    es_principal: Optional[bool]
    notas: Optional[str]
    subido_por: Optional[int]

class ArchivoMoldeCreate(ArchivoMoldeBase): archivo: bytes
class ArchivoMoldeOut(ArchivoMoldeBase):
    id_archivo: int
    fecha_subida: datetime
    class Config: orm_mode = True

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

class MuestraCreate(MuestraBase): pass
class MuestraUpdate(BaseModel):
    nombre_muestra: Optional[str]
    descripcion: Optional[str]
    talla: Optional[str]
    color: Optional[str]
    material: Optional[str]
    estado: Optional[str]
    feedback_cliente: Optional[str]
    feedback_interno: Optional[str]
    costo: Optional[float]

class MuestraOut(MuestraBase):
    id_muestra: int
    fecha_creacion: datetime
    fecha_entrega_estimada: Optional[datetime]
    fecha_entrega_real: Optional[datetime]
    class Config: orm_mode = True

class ImagenMuestraBase(BaseModel):
    id_muestra: int
    nombre_imagen: Optional[str]
    descripcion: Optional[str]
    es_principal: Optional[bool]
    orden_visualizacion: Optional[int]
    subido_por: Optional[int]

class ImagenMuestraCreate(ImagenMuestraBase): imagen: bytes
class ImagenMuestraOut(ImagenMuestraBase):
    id_imagen: int
    fecha_subida: datetime
    class Config: orm_mode = True

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

class TallerCreate(TallerBase): pass
class TallerUpdate(TallerBase): pass
class TallerOut(TallerBase):
    id_taller: int
    fecha_reg: datetime
    class Config: orm_mode = True

class EtapaBase(BaseModel):
    nombre: str
    descripcion: Optional[str]
    orden: Optional[int]
    tiempo_estim: Optional[float]
    activo: Optional[bool]

class EtapaCreate(EtapaBase): pass
class EtapaUpdate(EtapaBase): pass
class EtapaOut(EtapaBase):
    id_etapa: int
    class Config: orm_mode = True

class PlanBase(BaseModel):
    codigo_plan: str
    id_proyecto: int
    id_taller: Optional[int]
    fecha_ini_est: Optional[datetime.date]
    fecha_fin_est: Optional[datetime.date]
    estado: Optional[str]
    cantidad_prod: int
    prioridad: Optional[str]
    notas: Optional[str]
    costo_est: Optional[float]
    responsable: Optional[str]
    creado_por: Optional[int]

class PlanCreate(PlanBase): pass
class PlanUpdate(BaseModel):
    estado: Optional[str]
    cantidad_comp: Optional[int]
    notas: Optional[str]
    costo_real: Optional[float]

class PlanOut(PlanBase):
    id_plan: int
    cantidad_comp: int
    fecha_ini_real: Optional[datetime.date]
    fecha_fin_real: Optional[datetime.date]
    fecha_creacion: datetime
    class Config: orm_mode = True

class DetallePlanBase(BaseModel):
    id_plan: int
    id_etapa: int
    fecha_ini_est: Optional[datetime.date]
    fecha_fin_est: Optional[datetime.date]
    estado: Optional[str]
    responsable: Optional[str]
    observaciones: Optional[str]
    tiempo_inv: Optional[float]
    pct_completado: Optional[float]

class DetallePlanCreate(DetallePlanBase): pass
class DetallePlanUpdate(BaseModel):
    estado: Optional[str]
    responsable: Optional[str]
    tiempo_inv: Optional[float]
    pct_completado: Optional[float]

class DetallePlanOut(DetallePlanBase):
    id_detalle: int
    class Config: orm_mode = True

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

class MaterialCreate(MaterialBase): pass
class MaterialUpdate(BaseModel):
    stock_actual: Optional[float]
    stock_minimo: Optional[float]
    costo_unitario: Optional[float]
    estado: Optional[str]

class MaterialOut(MaterialBase):
    id_material: int
    fecha_registro: datetime
    class Config: orm_mode = True

class MatProyectoBase(BaseModel):
    id_proyecto: int
    id_material: int
    cantidad_req: float
    notas: Optional[str]

class MatProyectoCreate(MatProyectoBase):
    costo_unit: Optional[float]
class MatProyectoUpdate(BaseModel):
    cantidad_uso: Optional[float]
    costo_total: Optional[float]

class MatProyectoOut(MatProyectoBase):
    id_mat_proy: int
    cantidad_uso: Optional[float]
    costo_total: Optional[float]
    fecha_asig: datetime.date
    class Config: orm_mode = True

# Branding proyectos
class BrandingProyectoBase(BaseModel):
    id_proyecto: int
    tipo_servicio: str
    brief_cliente: Optional[str]
    objetivos: Optional[str]
    publico_objetivo: Optional[str]
    competencia: Optional[str]
    referencias_visuales: Optional[str]
    fecha_inicio: Optional[datetime.date]
    fecha_entrega_estimada: Optional[datetime.date]
    fecha_entrega_real: Optional[datetime.date]
    estado: Optional[str]
    numero_revisiones: Optional[int]
    revisiones_incluidas: Optional[int]
    feedback_cliente: Optional[str]
    notas_internas: Optional[str]
    responsable_diseno: Optional[str]

class BrandingProyectoCreate(BrandingProyectoBase):
    pass

class BrandingProyectoUpdate(BaseModel):
    id_proyecto: Optional[int]
    tipo_servicio: Optional[str]
    brief_cliente: Optional[str]
    objetivos: Optional[str]
    publico_objetivo: Optional[str]
    competencia: Optional[str]
    referencias_visuales: Optional[str]
    fecha_inicio: Optional[datetime.date]
    fecha_entrega_estimada: Optional[datetime.date]
    fecha_entrega_real: Optional[datetime.date]
    estado: Optional[str]
    numero_revisiones: Optional[int]
    revisiones_incluidas: Optional[int]
    feedback_cliente: Optional[str]
    notas_internas: Optional[str]
    responsable_diseno: Optional[str]

class BrandingProyectoOut(BrandingProyectoBase):
    id_proyecto_branding: int
    class Config:
        orm_mode = True


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

class EntregableOut(EntregableBase):
    id_entregable: int
    fecha_creacion: datetime
    class Config:
        orm_mode = True


# Branding revisiones
class RevisionBase(BaseModel):
    id_proyecto_branding: int
    numero_revision: int
    tipo_revision: str
    comentarios: Optional[str]
    cambios_solicitados: Optional[str]
    estado: Optional[str]
    fecha_limite: Optional[datetime.date]
    revisor: Optional[str]

class RevisionCreate(RevisionBase):
    pass

class RevisionOut(RevisionBase):
    id_revision: int
    fecha_revision: datetime
    archivos_revision: Optional[bytes]
    nombre_archivos: Optional[str]
    class Config:
        orm_mode = True


# Branding feedback fechas
class FeedbackFechaBase(BaseModel):
    id_proyecto_branding: int
    fecha_feedback: datetime.date
    comentario: str
    prioridad: Optional[str]
    estado: Optional[str]
    creado_por: Optional[int]

class FeedbackFechaCreate(FeedbackFechaBase):
    pass

class FeedbackFechaOut(FeedbackFechaBase):
    id_feedback: int
    fecha_creacion: datetime
    class Config:
        orm_mode = True

# Proyecto
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
        orm_mode = True

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
        orm_mode = True

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

class EcommerceDocumentoOut(EcommerceDocumentoBase):
    id_documento: int
    nombre_archivo: str
    extension: str
    tamano_archivo: int
    fecha_subida: datetime
    class Config:
        orm_mode = True

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
        orm_mode = True

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

class FacturaCreate(FacturaBase): pass

class FacturaUpdate(BaseModel):
    serie: Optional[str]
    folio: Optional[int]
    fecha_vencimiento: Optional[date]
    fecha_pago: Optional[date]
    subtotal: Optional[float]
    descuento: Optional[float]
    impuestos: Optional[float]
    total: Optional[float]
    estado: Optional[str]
    metodo_pago: Optional[str]
    forma_pago: Optional[str]
    condiciones_pago: Optional[str]
    notas: Optional[str]
    uuid_sat: Optional[str]
    archivo_xml: Optional[bytes]
    archivo_pdf: Optional[bytes]
    nombre_archivo_pdf: Optional[str]

class FacturaOut(FacturaBase):
    id_factura: int
    fecha_creacion: datetime
    class Config:
        orm_mode = True

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

class PagoCreate(PagoBase): pass

class PagoUpdate(BaseModel):
    monto: Optional[float]
    fecha_pago: Optional[date]
    metodo_pago: Optional[str]
    forma_pago: Optional[str]
    referencia: Optional[str]
    banco: Optional[str]
    cuenta: Optional[str]
    comprobante: Optional[bytes]
    nombre_comprobante: Optional[str]
    notas: Optional[str]

class PagoOut(PagoBase):
    id_pago: int
    fecha_registro: datetime
    class Config:
        orm_mode = True

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

class GastoCreate(GastoBase): pass

class GastoUpdate(BaseModel):
    concepto: Optional[str]
    descripcion: Optional[str]
    monto: Optional[float]
    fecha_gasto: Optional[date]
    categoria: Optional[str]
    proveedor: Optional[str]
    metodo_pago: Optional[str]
    deducible: Optional[bool]
    comprobante: Optional[bytes]
    nombre_comprobante: Optional[str]
    notas: Optional[str]

class GastoOut(GastoBase):
    id_gasto: int
    fecha_registro: datetime
    class Config:
        orm_mode = True

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

class CuentaCobrarCreate(CuentaCobrarBase): pass

class CuentaCobrarUpdate(BaseModel):
    monto: Optional[float]
    saldo_pendiente: Optional[float]
    fecha_vencimiento: Optional[date]
    dias_vencido: Optional[int]
    estado: Optional[str]
    notas: Optional[str]

class CuentaCobrarOut(CuentaCobrarBase):
    id_cuenta_cobrar: int
    class Config:
        orm_mode = True