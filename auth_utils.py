import jwt
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import models

# Configuración
SECRET_KEY = "0x4B29Cca180391217A08Bc8ecD9EA0c4397dB9AB1"  # Cambiar en producción
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generar hash de contraseña"""
    return pwd_context.hash(password)

def create_access_token(data: Dict[Any, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Crear token JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Verificar y decodificar token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None

def generate_reset_token() -> str:
    """Generar token de reset de contraseña"""
    return secrets.token_urlsafe(32)

def is_user_locked(usuario: models.Usuario) -> bool:
    """Verificar si el usuario está bloqueado"""
    if usuario.bloqueado_hasta:
        return datetime.utcnow() < usuario.bloqueado_hasta
    return False

def should_lock_user(usuario: models.Usuario) -> bool:
    """Determinar si el usuario debe ser bloqueado"""
    return usuario.intentos_login >= MAX_LOGIN_ATTEMPTS

def lock_user(db: Session, usuario: models.Usuario) -> None:
    """Bloquear usuario por intentos fallidos"""
    usuario.bloqueado_hasta = datetime.utcnow() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
    db.commit()

def reset_login_attempts(db: Session, usuario: models.Usuario) -> None:
    """Resetear intentos de login"""
    usuario.intentos_login = 0
    usuario.bloqueado_hasta = None
    db.commit()

def increment_login_attempts(db: Session, usuario: models.Usuario) -> None:
    """Incrementar intentos de login fallidos"""
    usuario.intentos_login += 1
    
    if should_lock_user(usuario):
        lock_user(db, usuario)
    else:
        db.commit()

def authenticate_user(db: Session, email: str, password: str) -> Optional[models.Usuario]:
    """Autenticar usuario"""
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == email
    ).first()
    
    if not usuario:
        return None
    
    # Verificar si el usuario está bloqueado
    if is_user_locked(usuario):
        return None
    
    # Verificar contraseña
    if not verify_password(password, usuario.contrasena):
        increment_login_attempts(db, usuario)
        return None
    
    # Login exitoso - resetear intentos
    reset_login_attempts(db, usuario)
    
    # Actualizar último acceso
    usuario.fecha_ultimo_acceso = datetime.utcnow()
    db.commit()
    
    return usuario

def create_user_info_dict(usuario: models.Usuario) -> Dict[str, Any]:
    """Crear diccionario con información del usuario"""
    return {
        "id_usuario": usuario.id_usuario,
        "nombre": usuario.nombre,
        "apellidos": usuario.apellidos,
        "email": usuario.email,
        "cargo": usuario.cargo,
        "departamento": usuario.departamento,
        "id_rol": usuario.id_rol
    }

def get_user_by_reset_token(db: Session, token: str) -> Optional[models.Usuario]:
    """Obtener usuario por token de reset"""
    usuario = db.query(models.Usuario).filter(
        models.Usuario.token_reset == token,
        models.Usuario.fecha_expiracion_token > datetime.utcnow()
    ).first()
    
    return usuario

def clear_reset_token(db: Session, usuario: models.Usuario) -> None:
    """Limpiar token de reset"""
    usuario.token_reset = None
    usuario.fecha_expiracion_token = None
    db.commit()

def set_reset_token(db: Session, usuario: models.Usuario) -> str:
    """Establecer token de reset"""
    token = generate_reset_token()
    usuario.token_reset = token
    usuario.fecha_expiracion_token = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    return token