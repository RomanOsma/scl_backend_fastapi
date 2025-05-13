# app/security/auth_security.py

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt # Para codificar y decodificar JWTs
from passlib.context import CryptContext # Para hashear y verificar contraseñas

from app.core.config import settings # Para acceder a JWT_SECRET_KEY, ALGORITHM, etc.

# Configuración para el hashing de contraseñas usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña en texto plano contra una contraseña hasheada.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception: # Captura errores generales, por ejemplo, si el hash no es bcrypt.
        return False

def get_password_hash(password: str) -> str:
    """
    Genera un hash para una contraseña dada usando bcrypt.
    """
    return pwd_context.hash(password)

# --- Funciones Específicas de JWT ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un nuevo token de acceso JWT.

    :param data: Diccionario con los datos a incluir en el payload del token (ej: {"sub": username}).
    :param expires_delta: Opcional. Un timedelta para la duración del token.
                          Si no se provee, usa ACCESS_TOKEN_EXPIRE_MINUTES de la configuración.
    :return: El token JWT codificado como string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)}) # exp: expiration time, iat: issued at
    
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodifica un token de acceso JWT.
    Verifica la firma y la expiración.

    :param token: El token JWT como string.
    :return: El payload (diccionario) del token si es válido y no ha expirado, sino None.
    """
    try:
        # Intenta decodificar el token. jwt.decode verifica la firma y la expiración.
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Podrías añadir más validaciones aquí si es necesario (ej: verificar 'iss' o 'aud')
        return payload
    except JWTError: # Esto captura errores de firma inválida, token expirado, etc.
        return None