from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Date, Enum as SAEnum, Boolean
from sqlalchemy.types import DECIMAL, JSON, LargeBinary
from sqlalchemy.sql import func
import enum
from database import Base

class ClienteEstado(enum.Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"
    POTENCIAL = "POTENCIAL"

class ClienteTipo(enum.Enum):
    CONFECCION = "CONFECCION"
    MOLDERIA = "MOLDERIA"
    BRANDING = "BRANDING"
    ECOMMERCE = "ECOMMERCE"
    MULTIPLE = "MULTIPLE"

class CRMCliente(Base):
    __tablename__ = "CRM_CLIENTES"

    id_cliente = Column("ID_CLIENTE", Integer, primary_key=True, index=True)
    nombre = Column("NOMBRE", String(100), nullable=False)
    nombre_contacto = Column("NOMBRE_CONTACTO", String(100))
    email = Column("EMAIL", String(100), index=True)
    telefono = Column("TELEFONO", String(20))
    direccion = Column("DIRECCION", Text)
    ciudad = Column("CIUDAD", String(50))
    pais = Column("PAIS", String(50))
    codigo_postal = Column("CODIGO_POSTAL", String(20))
    rfc = Column("RFC", String(20))
    estado = Column("ESTADO", SAEnum(ClienteEstado), default=ClienteEstado.ACTIVO)
    fecha_registro = Column("FECHA_REGISTRO", DateTime, server_default=func.now())
    fecha_actualizacion = Column("FECHA_ACTUALIZACION", DateTime, server_default=func.now(), onupdate=func.now())
    notas = Column("NOTAS", Text)
    tipo_cliente = Column("TIPO_CLIENTE", SAEnum(ClienteTipo), nullable=False)
    creado_por = Column("CREADO_POR", Integer)

class UsuarioEstado(enum.Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"
    SUSPENDIDO = "SUSPENDIDO"

class Usuario(Base):
    __tablename__ = "USUARIOS"

    id_usuario = Column("ID_USUARIO", Integer, primary_key=True, index=True)
    nombre = Column("NOMBRE", String(100), nullable=False)
    apellidos = Column("APELLIDOS", String(100))
    email = Column("EMAIL", String(100), unique=True, index=True, nullable=False)
    contrasena = Column("CONTRASEÑA", String(255), nullable=False)
    id_rol = Column("ID_ROL", Integer, nullable=False)
    telefono = Column("TELEFONO", String(20))
    cargo = Column("CARGO", String(100))
    departamento = Column("DEPARTAMENTO", String(100))
    fecha_registro = Column("FECHA_REGISTRO", DateTime, server_default=func.now())
    fecha_ultimo_acceso = Column("FECHA_ULTIMO_ACCESO", DateTime)
    estado = Column("ESTADO", SAEnum(UsuarioEstado), default=UsuarioEstado.ACTIVO)
    foto_perfil = Column("FOTO_PERFIL", LargeBinary)
    intentos_login = Column("INTENTOS_LOGIN", Integer, default=0)
    bloqueado_hasta = Column("BLOQUEADO_HASTA", DateTime)
    token_reset = Column("TOKEN_RESET", String(255))
    fecha_expiracion_token = Column("FECHA_EXPIRACION_TOKEN", DateTime)
    configuracion_notificaciones = Column("CONFIGURACION_NOTIFICACIONES", JSON)
    creado_por = Column("CREADO_POR", Integer)

class ProyectoTipo(Base):
    __tablename__ = "PROYECTOS_TIPOS"
    id_tipo_proyecto = Column("ID_TIPO_PROYECTO", Integer, primary_key=True, index=True)
    nombre = Column("NOMBRE", String(50), nullable=False)
    descripcion = Column("DESCRIPCION", Text)
    activo = Column("ACTIVO", Boolean, default=True)

class Proyecto(Base):
    __tablename__ = "PROYECTOS_PEDIDOS"
    id_proyecto = Column("ID_PROYECTO", Integer, primary_key=True, index=True)
    codigo_proyecto = Column("CODIGO_PROYECTO", String(50), unique=True, nullable=False)
    id_cliente = Column("ID_CLIENTE", Integer, nullable=False)
    nombre_proyecto = Column("NOMBRE_PROYECTO", String(100), nullable=False)
    id_tipo_proyecto = Column("ID_TIPO_PROYECTO", Integer, nullable=False)
    descripcion = Column("DESCRIPCION", Text)
    especificaciones_tecnicas = Column("ESPECIFICACIONES_TECNICAS", Text)
    fecha_inicio = Column("FECHA_INICIO", DateTime)
    fecha_entrega_estimada = Column("FECHA_ENTREGA_ESTIMADA", DateTime)
    fecha_entrega_real = Column("FECHA_ENTREGA_REAL", DateTime)
    fecha_finalizacion = Column("FECHA_FINALIZACION", DateTime)
    estado = Column("ESTADO", SAEnum(
        'PRESUPUESTO','EN_PROCESO','APROBADO','FINALIZADO','CANCELADO','PAUSADO',
        name="proyecto_estado"), default='PRESUPUESTO')
    prioridad = Column("PRIORIDAD", SAEnum(
        'BAJA','MEDIA','ALTA','URGENTE', name="proyecto_prioridad"), default='MEDIA')
    progreso_porcentaje = Column("PROGRESO_PORCENTAJE", DECIMAL(5,2), default=0)
    notas = Column("NOTAS", Text)
    fecha_creacion = Column("FECHA_CREACION", DateTime, server_default=func.now())
    fecha_actualizacion = Column("FECHA_ACTUALIZACION", DateTime,
                                 server_default=func.now(), onupdate=func.now())
    creado_por = Column("CREADO_POR", Integer)

class MoldeEstado(enum.Enum):
    EN_DESARROLLO = "EN_DESARROLLO"
    REVISION = "REVISION"
    APROBADO = "APROBADO"
    OBSOLETO = "OBSOLETO"

class ArchivoTipo(enum.Enum):
    DXF = "DXF"
    PDF = "PDF"
    AI = "AI"
    PLT = "PLT"
    AAMA = "AAMA"
    OTROS = "OTROS"

class MuestraEstado(enum.Enum):
    PLANIFICADA = "PLANIFICADA"
    EN_CONFECCION = "EN_CONFECCION"
    COMPLETADA = "COMPLETADA"
    PENDIENTE_APROBACION = "PENDIENTE_APROBACION"
    APROBADA = "APROBADA"
    RECHAZADA = "RECHAZADA"

class MolderiaMolde(Base):
    __tablename__ = "MOLDERIA_MOLDES"
    id_molde = Column("ID_MOLDE", Integer, primary_key=True, index=True)
    codigo_molde = Column("CODIGO_MOLDE", String(50), unique=True, nullable=False)
    id_proyecto = Column("ID_PROYECTO", Integer, nullable=False)
    nombre_molde = Column("NOMBRE_MOLDE", String(100), nullable=False)
    categoria = Column("CATEGORIA", String(50))
    talla = Column("TALLA", String(20))
    version = Column("VERSION", String(20), default="1.0")
    estado = Column("ESTADO", SAEnum(MoldeEstado), default=MoldeEstado.EN_DESARROLLO)
    fecha_creacion = Column("FECHA_CREACION", DateTime, server_default=func.now())
    fecha_modificacion = Column("FECHA_ULTIMA_MODIFICACION", DateTime, server_default=func.now(), onupdate=func.now())
    notas = Column("NOTAS", Text)
    medidas = Column("MEDIDAS", Text)
    observaciones_tecnicas = Column("OBSERVACIONES_TECNICAS", Text)
    creado_por = Column("CREADO_POR", Integer)

class MolderiaArchivo(Base):
    __tablename__ = "MOLDERIA_ARCHIVOS"
    id_archivo = Column("ID_ARCHIVO_MOLDE", Integer, primary_key=True, index=True)
    id_molde = Column("ID_MOLDE", Integer, nullable=False)
    nombre_archivo = Column("NOMBRE_ARCHIVO", String(200), nullable=False)
    tipo_archivo = Column("TIPO_ARCHIVO", SAEnum(ArchivoTipo), nullable=False)
    archivo = Column("ARCHIVO", LargeBinary, nullable=False)
    fecha_subida = Column("FECHA_SUBIDA", DateTime, server_default=func.now())
    version = Column("VERSION", String(20))
    es_principal = Column("ES_PRINCIPAL", Boolean, default=False)
    notas = Column("NOTAS", Text)
    subido_por = Column("SUBIDO_POR", Integer)

class MolderiaMuestra(Base):
    __tablename__ = "MOLDERIA_MUESTRAS"
    id_muestra = Column("ID_MUESTRA", Integer, primary_key=True, index=True)
    codigo_muestra = Column("CODIGO_MUESTRA", String(50), unique=True, nullable=False)
    id_proyecto = Column("ID_PROYECTO", Integer, nullable=False)
    id_molde = Column("ID_MOLDE", Integer)
    nombre_muestra = Column("NOMBRE_MUESTRA", String(100), nullable=False)
    descripcion = Column("DESCRIPCION", Text)
    talla = Column("TALLA", String(20))
    color = Column("COLOR", String(50))
    material = Column("MATERIAL", String(100))
    fecha_creacion = Column("FECHA_CREACION", DateTime, server_default=func.now())
    fecha_entrega_estimada = Column("FECHA_ENTREGA_ESTIMADA", DateTime)
    fecha_entrega_real = Column("FECHA_ENTREGA_REAL", DateTime)
    estado = Column("ESTADO", SAEnum(MuestraEstado), default=MuestraEstado.PLANIFICADA)
    feedback_cliente = Column("FEEDBACK_CLIENTE", Text)
    feedback_interno = Column("FEEDBACK_INTERNO", Text)
    costo = Column("COSTO", DECIMAL(10, 2))
    creada_por = Column("CREADA_POR", Integer)

class MolderiaImagenMuestra(Base):
    __tablename__ = "MOLDERIA_IMAGENES_MUESTRAS"
    id_imagen = Column("ID_IMAGEN", Integer, primary_key=True, index=True)
    id_muestra = Column("ID_MUESTRA", Integer, nullable=False)
    imagen = Column("IMAGEN", LargeBinary, nullable=False)
    nombre_imagen = Column("NOMBRE_IMAGEN", String(200))
    descripcion = Column("DESCRIPCION", Text)
    fecha_subida = Column("FECHA_SUBIDA", DateTime, server_default=func.now())
    es_principal = Column("ES_PRINCIPAL", Boolean, default=False)
    orden_visualizacion = Column("ORDEN_VISUALIZACION", Integer, default=0)
    subido_por = Column("SUBIDO_POR", Integer)

class TallerEstado(enum.Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"
    MANTENIMIENTO = "MANTENIMIENTO"

class ProduccionTaller(Base):
    __tablename__ = "PRODUCCION_TALLERES"
    id = Column(Integer, name="ID_TALLER", primary_key=True, index=True)  # Cambiar aquí
    nombre        = Column(String(100), nullable=False)
    codigo        = Column(String(20), unique=True)
    direccion     = Column(Text)
    contacto      = Column(String(100))
    telefono      = Column(String(20))
    email         = Column(String(100))
    especialidad  = Column(String(100))
    capacidad     = Column(Integer)
    estado        = Column(SAEnum(TallerEstado), default=TallerEstado.ACTIVO)
    calificacion  = Column(DECIMAL(3,2))
    notas         = Column(Text)
    fecha_reg     = Column(DateTime, server_default=func.now())

class ProduccionEtapa(Base):
    __tablename__ = "PRODUCCION_ETAPAS"
    id_etapa      = Column(Integer, name="ID_ETAPA", primary_key=True, index=True)
    nombre        = Column(String(50), nullable=False)
    descripcion   = Column(Text)
    orden         = Column(Integer)
    tiempo_estim  = Column(DECIMAL(6,2))
    activo        = Column(Boolean, default=True)

class ProduccionPlan(Base):
    __tablename__ = "PRODUCCION_PLANES"
    id_plan        = Column(Integer, name="ID_PLAN", primary_key=True, index=True)
    codigo_plan    = Column(String(50), unique=True, nullable=False)
    id_proyecto    = Column(Integer, ForeignKey("PROYECTOS_PEDIDOS.ID_PROYECTO"))
    id_taller      = Column(Integer, ForeignKey("PRODUCCION_TALLERES.ID_TALLER"))
    fecha_ini_est  = Column(Date)
    fecha_fin_est  = Column(Date)
    fecha_ini_real = Column(Date)
    fecha_fin_real = Column(Date)
    estado         = Column(SAEnum('PLANIFICADO','EN_PROCESO','COMPLETADO','PAUSADO','CANCELADO', name="produccion_plan_estado"), default='PLANIFICADO')
    cantidad_prod  = Column(Integer, nullable=False)
    cantidad_comp  = Column(Integer, default=0)
    prioridad      = Column(SAEnum('BAJA','MEDIA','ALTA','URGENTE', name="produccion_plan_prioridad"), default='MEDIA')
    notas          = Column(Text)
    costo_est      = Column(DECIMAL(12,2))
    costo_real     = Column(DECIMAL(12,2))
    responsable    = Column(String(100))
    creado_por     = Column(Integer)
    fecha_creacion = Column(DateTime, server_default=func.now())

class ProduccionDetallePlan(Base):
    __tablename__ = "PRODUCCION_DETALLE_PLAN"
    id_detalle     = Column(Integer, name="ID_DETALLE_PLAN", primary_key=True, index=True)
    id_plan        = Column(Integer, ForeignKey("PRODUCCION_PLANES.ID_PLAN", ondelete="CASCADE"))
    id_etapa       = Column(Integer, ForeignKey("PRODUCCION_ETAPAS.ID_ETAPA"))
    fecha_ini_est  = Column(Date)
    fecha_fin_est  = Column(Date)
    fecha_ini_real = Column(Date)
    fecha_fin_real = Column(Date)
    estado         = Column(SAEnum('PENDIENTE','EN_PROCESO','COMPLETADO','PAUSADO', name="produccion_detalle_estado"), default='PENDIENTE')
    responsable    = Column(String(100))
    observaciones  = Column(Text)
    tiempo_inv     = Column(DECIMAL(6,2))
    pct_completado = Column(DECIMAL(5,2), default=0)

class ProduccionMaterial(Base):
    __tablename__ = "PRODUCCION_MATERIALES"
    id_material    = Column(Integer, name="ID_MATERIAL", primary_key=True, index=True)
    codigo_material= Column(String(50), unique=True, nullable=False)
    nombre         = Column(String(100), nullable=False)
    descripcion    = Column(Text)
    categoria      = Column(String(50))
    unidad_medida  = Column(String(20))
    stock_actual   = Column(DECIMAL(10,2), default=0)
    stock_minimo   = Column(DECIMAL(10,2), default=0)
    costo_unitario = Column(DECIMAL(10,2))
    proveedor      = Column(String(100))
    estado         = Column(SAEnum('ACTIVO','INACTIVO','DESCONTINUADO', name="produccion_material_estado"), default='ACTIVO')
    fecha_registro = Column(DateTime, server_default=func.now())

class ProduccionMaterialProyecto(Base):
    __tablename__ = "PRODUCCION_MATERIALES_PROYECTO"
    id_mat_proy    = Column(Integer, name="ID_MATERIAL_PROYECTO", primary_key=True, index=True)
    id_proyecto    = Column(Integer, ForeignKey("PROYECTOS_PEDIDOS.ID_PROYECTO"))
    id_material    = Column(Integer, ForeignKey("PRODUCCION_MATERIALES.ID_MATERIAL"))
    cantidad_req   = Column(DECIMAL(10,2), nullable=False)
    cantidad_uso   = Column(DECIMAL(10,2), default=0)
    costo_unit     = Column(DECIMAL(10,2))
    costo_total    = Column(DECIMAL(12,2))
    fecha_asig     = Column(Date, server_default=func.current_date())
    notas          = Column(Text)


class ServicioTipo(enum.Enum):
    LOGO = "LOGO"
    PALETA_COLORES = "PALETA_COLORES"
    EMPAQUES = "EMPAQUES"
    ETIQUETAS = "ETIQUETAS"
    MANUAL_MARCA = "MANUAL_MARCA"
    COMPLETO = "COMPLETO"
    REDISEÑO = "REDISEÑO"

class BrandingEstado(enum.Enum):
    BRIEF = "BRIEF"
    EN_DISENO = "EN_DISENO"
    REVISION_INTERNA = "REVISION_INTERNA"
    PRESENTACION_CLIENTE = "PRESENTACION_CLIENTE"
    REVISION_CLIENTE = "REVISION_CLIENTE"
    APROBADO = "APROBADO"
    FINALIZADO = "FINALIZADO"

class EntregableTipo(enum.Enum):
    MANUAL = "MANUAL"
    LOGO = "LOGO"
    ARTE_FINAL = "ARTE_FINAL"
    MOCKUP = "MOCKUP"
    PRESENTACION = "PRESENTACION"
    PALETA_COLORES = "PALETA_COLORES"
    TIPOGRAFIA = "TIPOGRAFIA"
    APLICACIONES = "APLICACIONES"

class EntregableEstado(enum.Enum):
    BORRADOR = "BORRADOR"
    REVISION = "REVISION"
    APROBADO = "APROBADO"
    ENTREGADO = "ENTREGADO"

class TipoRevision(enum.Enum):
    INTERNA = "INTERNA"
    CLIENTE = "CLIENTE"

class RevisionEstado(enum.Enum):
    PENDIENTE = "PENDIENTE"
    EN_PROCESO = "EN_PROCESO"
    COMPLETADA = "COMPLETADA"

class FeedbackPrioridad(enum.Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"

class FeedbackEstado(enum.Enum):
    PENDIENTE = "PENDIENTE"
    EN_PROCESO = "EN_PROCESO"
    COMPLETADO = "COMPLETADO"


class BrandingProyecto(Base):
    __tablename__ = "BRANDING_PROYECTOS"

    id_proyecto_branding = Column("ID_PROYECTO_BRANDING", Integer, primary_key=True, index=True)
    id_proyecto = Column("ID_PROYECTO", Integer, ForeignKey("PROYECTOS_PEDIDOS.ID_PROYECTO"))
    tipo_servicio = Column("TIPO_SERVICIO", SAEnum(ServicioTipo), nullable=False)
    brief_cliente = Column("BRIEF_CLIENTE", Text)
    objetivos = Column("OBJETIVOS", Text)
    publico_objetivo = Column("PUBLICO_OBJETIVO", Text)
    competencia = Column("COMPETENCIA", Text)
    referencias_visuales = Column("REFERENCIAS_VISUALES", Text)
    fecha_inicio = Column("FECHA_INICIO", Date)
    fecha_entrega_estimada = Column("FECHA_ENTREGA_ESTIMADA", Date)
    fecha_entrega_real = Column("FECHA_ENTREGA_REAL", Date)
    estado = Column("ESTADO", SAEnum(BrandingEstado), default=BrandingEstado.BRIEF)
    numero_revisiones = Column("NUMERO_REVISIONES", Integer, default=0)
    revisiones_incluidas = Column("REVISIONES_INCLUIDAS", Integer, default=3)
    feedback_cliente = Column("FEEDBACK_CLIENTE", Text)
    notas_internas = Column("NOTAS_INTERNAS", Text)
    responsable_diseno = Column("RESPONSABLE_DISEÑO", String(100))


class BrandingEntregable(Base):
    __tablename__ = "BRANDING_ENTREGABLES"

    id_entregable = Column("ID_ENTREGABLE", Integer, primary_key=True, index=True)
    id_proyecto_branding = Column("ID_PROYECTO_BRANDING", Integer, ForeignKey("BRANDING_PROYECTOS.ID_PROYECTO_BRANDING", ondelete="CASCADE"))
    nombre_entregable = Column("NOMBRE_ENTREGABLE", String(200), nullable=False)
    tipo_entregable = Column("TIPO_ENTREGABLE", SAEnum(EntregableTipo), nullable=False)
    descripcion = Column("DESCRIPCION", Text)
    archivo = Column("ARCHIVO", LargeBinary, nullable=False)
    nombre_archivo = Column("NOMBRE_ARCHIVO", String(255))
    extension = Column("EXTENSION", String(10))
    tamano_archivo = Column("TAMAÑO_ARCHIVO", Integer)
    fecha_creacion = Column("FECHA_CREACION", DateTime, server_default=func.now())
    version = Column("VERSION", String(20), default="1.0")
    estado = Column("ESTADO", SAEnum(EntregableEstado), default=EntregableEstado.BORRADOR)
    creado_por = Column("CREADO_POR", Integer)


class BrandingRevision(Base):
    __tablename__ = "BRANDING_REVISIONES"

    id_revision = Column("ID_REVISION", Integer, primary_key=True, index=True)
    id_proyecto_branding = Column("ID_PROYECTO_BRANDING", Integer, ForeignKey("BRANDING_PROYECTOS.ID_PROYECTO_BRANDING", ondelete="CASCADE"))
    numero_revision = Column("NUMERO_REVISION", Integer, nullable=False)
    fecha_revision = Column("FECHA_REVISION", DateTime, server_default=func.now())
    tipo_revision = Column("TIPO_REVISION", SAEnum(TipoRevision), nullable=False)
    comentarios = Column("COMENTARIOS", Text)
    cambios_solicitados = Column("CAMBIOS_SOLICITADOS", Text)
    estado = Column("ESTADO", SAEnum(RevisionEstado), default=RevisionEstado.PENDIENTE)
    fecha_limite = Column("FECHA_LIMITE", Date)
    revisor = Column("REVISOR", String(100))
    archivos_revision = Column("ARCHIVOS_REVISION", LargeBinary)
    nombre_archivos = Column("NOMBRE_ARCHIVOS", String(255))


class BrandingFeedbackFecha(Base):
    __tablename__ = "BRANDING_FEEDBACK_FECHAS"

    id_feedback = Column("ID_FEEDBACK", Integer, primary_key=True, index=True)
    id_proyecto_branding = Column("ID_PROYECTO_BRANDING", Integer, ForeignKey("BRANDING_PROYECTOS.ID_PROYECTO_BRANDING", ondelete="CASCADE"))
    fecha_feedback = Column("FECHA_FEEDBACK", Date, nullable=False)
    comentario = Column("COMENTARIO", Text, nullable=False)
    prioridad = Column("PRIORIDAD", SAEnum(FeedbackPrioridad), default=FeedbackPrioridad.MEDIA)
    estado = Column("ESTADO", SAEnum(FeedbackEstado), default=FeedbackEstado.PENDIENTE)
    creado_por = Column("CREADO_POR", Integer)
    fecha_creacion = Column("FECHA_CREACION", DateTime, server_default=func.now())

class EcommerceProyectoEstado(enum.Enum):
    PLANIFICACION = "PLANIFICACION"
    DISENO = "DISENO"
    DESARROLLO = "DESARROLLO"
    CONTENIDO = "CONTENIDO"
    PRUEBAS = "PRUEBAS"
    CAPACITACION = "CAPACITACION"
    PUBLICADO = "PUBLICADO"
    MANTENIMIENTO = "MANTENIMIENTO"

class EcommercePlataforma(enum.Enum):
    SHOPIFY = "SHOPIFY"
    WOOCOMMERCE = "WOOCOMMERCE"
    MAGENTO = "MAGENTO"
    PRESTASHOP = "PRESTASHOP"
    WIXCOMMERCE = "WIXCOMMERCE"
    SQUARESPACE = "SQUARESPACE"
    OTRA = "OTRA"

class EcommerceProyecto(Base):
    __tablename__ = "ECOMMERCE_PROYECTOS"

    id_proyecto_ecommerce = Column(Integer, primary_key=True, index=True)
    id_proyecto = Column(Integer, ForeignKey("PROYECTOS_PEDIDOS.ID_PROYECTO"))
    nombre_tienda = Column(String(200))
    url_tienda = Column(String(255), nullable=True)
    dominio_principal = Column(String(255), nullable=True)
    plataforma = Column(SAEnum(EcommercePlataforma), nullable=False)
    plan_hosting = Column(String(100), nullable=True)
    funcionalidades_requeridas = Column(Text, nullable=True)
    numero_productos_estimado = Column(Integer, nullable=True)
    metodos_pago = Column(Text, nullable=True)
    metodos_envio = Column(Text, nullable=True)
    fecha_lanzamiento_estimada = Column(Date, nullable=True)
    fecha_lanzamiento_real = Column(Date, nullable=True)
    estado = Column(SAEnum(EcommerceProyectoEstado), default=EcommerceProyectoEstado.PLANIFICACION)
    ssl_configurado = Column(Boolean, default=False)
    analytics_configurado = Column(Boolean, default=False)
    seo_configurado = Column(Boolean, default=False)
    notas = Column(Text, nullable=True)
    responsable_desarrollo = Column(String(100), nullable=True)

class EcommerceCredencial(Base):
    __tablename__ = "ECOMMERCE_CREDENCIALES"

    id_credencial = Column(Integer, primary_key=True, index=True)
    id_proyecto_ecommerce = Column(Integer, ForeignKey("ECOMMERCE_PROYECTOS.id_proyecto_ecommerce"))
    tipo_credencial = Column(String(50), nullable=False)
    servicio = Column(String(100), nullable=True)
    usuario = Column(String(200), nullable=True)
    contrasena = Column(String(500), nullable=True)
    url_acceso = Column(String(255), nullable=True)
    email_recuperacion = Column(String(100), nullable=True)
    notas = Column(Text, nullable=True)
    fecha_expiracion = Column(Date, nullable=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, server_default=func.now())

class EcommerceDocumento(Base):
    __tablename__ = "ECOMMERCE_DOCUMENTOS"

    id_documento = Column(Integer, primary_key=True, index=True)
    id_proyecto_ecommerce = Column(Integer, ForeignKey("ECOMMERCE_PROYECTOS.id_proyecto_ecommerce"))
    nombre_documento = Column(String(200), nullable=False)
    tipo_documento = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=True)
    archivo = Column(LargeBinary, nullable=False)
    nombre_archivo = Column(String(255), nullable=False)
    extension = Column(String(10), nullable=False)
    tamano_archivo = Column(Integer, nullable=False)
    fecha_subida = Column(DateTime, server_default=func.now())
    version = Column(String(20), default="1.0")
    es_publico = Column(Boolean, default=False)
    subido_por = Column(Integer, nullable=True)

class EcommerceDatosMarca(Base):
    __tablename__ = "ECOMMERCE_DATOS_MARCA"

    id_datos_marca = Column(Integer, primary_key=True, index=True)
    id_proyecto_ecommerce = Column(Integer, ForeignKey("ECOMMERCE_PROYECTOS.id_proyecto_ecommerce"))
    email_marca = Column(String(200), nullable=True)
    contrasena_email = Column(String(500), nullable=True)
    servidor_smtp = Column(String(100), nullable=True)
    puerto_smtp = Column(Integer, nullable=True)
    configuracion_ssl = Column(Boolean, default=True)
    notas_email = Column(Text, nullable=True)
    fecha_configuracion = Column(DateTime, server_default=func.now())
    configurado_por = Column(Integer, nullable=True)

class FinancieroFactura(Base):
    __tablename__ = "FINANCIERO_FACTURAS"

    id_factura         = Column("ID_FACTURA", Integer, primary_key=True, index=True)
    numero_factura     = Column("NUMERO_FACTURA", String(50), unique=True, nullable=False)
    id_proyecto        = Column("ID_PROYECTO", Integer, ForeignKey("PROYECTOS.ID_PROYECTO"), nullable=False)
    serie              = Column("SERIE", String(20))
    folio              = Column("FOLIO", Integer)
    fecha_emision      = Column("FECHA_EMISION", Date, nullable=False)
    fecha_vencimiento  = Column("FECHA_VENCIMIENTO", Date)
    fecha_pago         = Column("FECHA_PAGO", Date)
    subtotal           = Column("SUBTOTAL", DECIMAL(18,2), nullable=False)
    descuento          = Column("DESCUENTO", DECIMAL(18,2), default=0)
    impuestos          = Column("IMPUESTOS", DECIMAL(18,2), nullable=False)
    total              = Column("TOTAL", DECIMAL(18,2), nullable=False)
    moneda             = Column("MONEDA", String(3), default="MXN")
    tipo_cambio        = Column("TIPO_CAMBIO", DECIMAL(18,4), default=1.0)
    estado             = Column("ESTADO", String(20), default="BORRADOR")
    metodo_pago        = Column("METODO_PAGO", String(50))
    forma_pago         = Column("FORMA_PAGO", String(50))
    condiciones_pago   = Column("CONDICIONES_PAGO", String(255))
    notas              = Column("NOTAS", Text)
    uuid_sat           = Column("UUID_SAT", String(100))
    archivo_xml        = Column("ARCHIVO_XML", LargeBinary)
    archivo_pdf        = Column("ARCHIVO_PDF", LargeBinary)
    nombre_archivo_pdf = Column("NOMBRE_ARCHIVO_PDF", String(255))
    creada_por         = Column("CREADA_POR", Integer, ForeignKey("USUARIOS.ID_USUARIO"))
    fecha_creacion     = Column("FECHA_CREACION", DateTime(timezone=True), server_default=func.now())


# ——— FINANCIERO_PAGOS ———
class FinancieroPago(Base):
    __tablename__ = "FINANCIERO_PAGOS"

    id_pago            = Column("ID_PAGO", Integer, primary_key=True, index=True)
    numero_pago        = Column("NUMERO_PAGO", String(50), unique=True, nullable=False)
    id_factura         = Column("ID_FACTURA", Integer, ForeignKey("FINANCIERO_FACTURAS.ID_FACTURA"), nullable=False)
    monto              = Column("MONTO", DECIMAL(18,2), nullable=False)
    fecha_pago         = Column("FECHA_PAGO", Date, nullable=False)
    metodo_pago        = Column("METODO_PAGO", String(50), nullable=False)
    forma_pago         = Column("FORMA_PAGO", String(50))
    referencia         = Column("REFERENCIA", String(100))
    banco              = Column("BANCO", String(100))
    cuenta             = Column("CUENTA", String(100))
    comprobante        = Column("COMPROBANTE", LargeBinary)
    nombre_comprobante = Column("NOMBRE_COMPROBANTE", String(255))
    notas              = Column("NOTAS", Text)
    registrado_por     = Column("REGISTRADO_POR", Integer, ForeignKey("USUARIOS.ID_USUARIO"))
    fecha_registro     = Column("FECHA_REGISTRO", DateTime(timezone=True), server_default=func.now())


# ——— FINANCIERO_GASTOS ———
class FinancieroGasto(Base):
    __tablename__ = "FINANCIERO_GASTOS"

    id_gasto           = Column("ID_GASTO", Integer, primary_key=True, index=True)
    numero_gasto       = Column("NUMERO_GASTO", String(50), unique=True, nullable=False)
    id_proyecto        = Column("ID_PROYECTO", Integer, ForeignKey("PROYECTOS.ID_PROYECTO"))
    concepto           = Column("CONCEPTO", String(255), nullable=False)
    descripcion        = Column("DESCRIPCION", Text)
    monto              = Column("MONTO", DECIMAL(18,2), nullable=False)
    moneda             = Column("MONEDA", String(3), default="MXN")
    fecha_gasto        = Column("FECHA_GASTO", Date, nullable=False)
    categoria          = Column("CATEGORIA", String(100), nullable=False)
    proveedor          = Column("PROVEEDOR", String(100))
    metodo_pago        = Column("METODO_PAGO", String(50))
    deducible          = Column("DEDUCIBLE", Boolean, default=True)
    comprobante        = Column("COMPROBANTE", LargeBinary)
    nombre_comprobante = Column("NOMBRE_COMPROBANTE", String(255))
    notas              = Column("NOTAS", Text)
    registrado_por     = Column("REGISTRADO_POR", Integer, ForeignKey("USUARIOS.ID_USUARIO"))
    fecha_registro     = Column("FECHA_REGISTRO", DateTime(timezone=True), server_default=func.now())


# ——— FINANCIERO_CUENTAS_COBRAR ———
class FinancieroCuentaCobrar(Base):
    __tablename__ = "FINANCIERO_CUENTAS_COBRAR"

    id_cuenta_cobrar  = Column("ID_CUENTA_COBRAR", Integer, primary_key=True, index=True)
    id_cliente        = Column("ID_CLIENTE", Integer, ForeignKey("CLIENTES.ID_CLIENTE"), nullable=False)
    id_factura        = Column("ID_FACTURA", Integer, ForeignKey("FINANCIERO_FACTURAS.ID_FACTURA"))
    concepto          = Column("CONCEPTO", String(255), nullable=False)
    monto             = Column("MONTO", DECIMAL(18,2), nullable=False)
    saldo_pendiente   = Column("SALDO_PENDIENTE", DECIMAL(18,2), nullable=False)
    fecha_vencimiento = Column("FECHA_VENCIMIENTO", Date, nullable=False)
    dias_vencido      = Column("DIAS_VENCIDO", Integer, default=0)
    estado            = Column("ESTADO", String(20), default="VIGENTE")
    notas             = Column("NOTAS", Text)
    fecha_creacion    = Column("FECHA_CREACION", DateTime(timezone=True), server_default=func.now())

class AuditLog(Base):
    __tablename__ = "AUDIT_LOGS"
    
    id = Column("ID", Integer, primary_key=True, index=True)
    endpoint = Column("ENDPOINT", String(255), nullable=False)
    method = Column("METHOD", String(10), nullable=False)
    api_key = Column("API_KEY", String(255), nullable=False)
    request_body = Column("REQUEST_BODY", Text)
    query_params = Column("QUERY_PARAMS", Text)
    user_agent = Column("USER_AGENT", String(500))
    ip_address = Column("IP_ADDRESS", String(45))
    status_code = Column("STATUS_CODE", Integer)
    timestamp = Column("TIMESTAMP", DateTime(timezone=True), nullable=False)
    
    # Índices para optimizar consultas
    __table_args__ = (
        {'mysql_engine': 'InnoDB'}
    )