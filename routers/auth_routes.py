from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta
import models
from schemas import LoginResponse, LoginRequest, UserInfo, TokenResponse, MessageResponse, ForgotPasswordRequest, ResetPasswordRequest
import auth_utils
from dependencies import get_db, get_api_key

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    dependencies=[Depends(get_api_key)]
)

# Lista negra de tokens (en producción usar Redis o base de datos)
blacklisted_tokens = set()

@router.post("/login", response_model=LoginResponse)
def login(
    request: Request,
    login_data: LoginRequest, 
    db: Session = Depends(get_db)
):
    """Iniciar sesión de usuario"""
    
    # Autenticar usuario
    usuario = auth_utils.authenticate_user(db, login_data.email, login_data.password)
    
    if not usuario:
        # Verificar si existe el usuario para dar mensaje específico
        user_exists = db.query(models.Usuario).filter(
            models.Usuario.email == login_data.email
        ).first()
        
        if user_exists and auth_utils.is_user_locked(user_exists):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario bloqueado por múltiples intentos fallidos. Intente más tarde."
            )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Verificar estado del usuario
    if usuario.estado != models.UsuarioEstado.ACTIVO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo o suspendido"
        )
    
    # Crear token de acceso
    token_data = {
        "user_id": usuario.id_usuario,
        "email": usuario.email,
        "rol": usuario.id_rol
    }
    
    access_token_expires = timedelta(minutes=auth_utils.TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data=token_data, 
        expires_delta=access_token_expires
    )
    
    # Crear información del usuario
    user_info = auth_utils.create_user_info_dict(usuario)
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=auth_utils.TOKEN_EXPIRE_MINUTES * 60,  # en segundos
        user=UserInfo(**user_info)
    )

@router.post("/logout", response_model=MessageResponse)
def logout(request: Request):
    """Cerrar sesión de usuario"""
    
    # Obtener token del header Authorization
    authorization = request.headers.get("authorization")
    
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        # Agregar token a lista negra
        blacklisted_tokens.add(token)
    
    return MessageResponse(message="Sesión cerrada exitosamente")

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: Request, db: Session = Depends(get_db)):
    """Renovar token de acceso"""
    
    authorization = request.headers.get("authorization")
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado"
        )
    
    token = authorization.split(" ")[1]
    
    # Verificar si el token está en lista negra
    if token in blacklisted_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    # Verificar token actual
    payload = auth_utils.verify_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado o inválido"
        )
    
    # Verificar que el usuario aún existe y está activo
    user_id = payload.get("user_id")
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == user_id
    ).first()
    
    if not usuario or usuario.estado != models.UsuarioEstado.ACTIVO:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no válido"
        )
    
    # Agregar token viejo a lista negra
    blacklisted_tokens.add(token)
    
    # Crear nuevo token
    token_data = {
        "user_id": usuario.id_usuario,
        "email": usuario.email,
        "rol": usuario.id_rol
    }
    
    access_token_expires = timedelta(minutes=auth_utils.TOKEN_EXPIRE_MINUTES)
    new_access_token = auth_utils.create_access_token(
        data=token_data, 
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=new_access_token,
        token_type="bearer",
        expires_in=auth_utils.TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(
    request_data: ForgotPasswordRequest, 
    db: Session = Depends(get_db)
):
    """Solicitar reset de contraseña"""
    
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == request_data.email
    ).first()
    
    # Por seguridad, siempre devolver el mismo mensaje
    if not usuario:
        return MessageResponse(
            message="Si el email existe, se ha enviado un enlace de recuperación"
        )
    
    # Generar token de reset
    reset_token = auth_utils.set_reset_token(db, usuario)
    
    # Aquí normalmente enviarías un email con el token
    # Por ahora solo lo loggeamos (NO hacer esto en producción)
    print(f"Token de reset para {usuario.email}: {reset_token}")
    
    return MessageResponse(
        message="Si el email existe, se ha enviado un enlace de recuperación"
    )

@router.post("/reset-password", response_model=MessageResponse)
def reset_password(
    request_data: ResetPasswordRequest, 
    db: Session = Depends(get_db)
):
    """Resetear contraseña con token"""
    
    usuario = auth_utils.get_user_by_reset_token(db, request_data.token)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado"
        )
    
    # Actualizar contraseña
    usuario.contrasena = auth_utils.get_password_hash(request_data.new_password)
    
    # Limpiar token de reset
    auth_utils.clear_reset_token(db, usuario)
    
    # Resetear intentos de login por si estaba bloqueado
    auth_utils.reset_login_attempts(db, usuario)
    
    return MessageResponse(
        message="Contraseña actualizada exitosamente"
    )

@router.get("/me", response_model=UserInfo)
def get_current_user_info(request: Request, db: Session = Depends(get_db)):
    """Obtener información del usuario actual"""
    
    authorization = request.headers.get("authorization")
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado"
        )
    
    token = authorization.split(" ")[1]
    
    # Verificar si el token está en lista negra
    if token in blacklisted_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    # Verificar token
    payload = auth_utils.verify_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado o inválido"
        )
    
    # Obtener usuario
    user_id = payload.get("user_id")
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == user_id
    ).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    user_info = auth_utils.create_user_info_dict(usuario)
    return UserInfo(**user_info)