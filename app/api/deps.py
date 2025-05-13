# app/api/deps.py

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer # Esquema de seguridad para Bearer Tokens
from sqlalchemy.orm import Session
from jose import JWTError # Para capturar errores de decodificación de JWT

from app.db.database import get_db
from app.db import models # Para tipar el objeto User que devolvemos
from app.schemas import token_schemas # Para TokenData (payload del token)
from app.security.auth_security import decode_access_token # Nuestra función para decodificar tokens
from app.crud import user_crud # Para obtener el usuario de la BD
from app.core.config import settings # Para obtener la URL del endpoint de token

# --- OAuth2PasswordBearer ---
# Esto crea un objeto que se puede usar como una dependencia.
# Le decimos a FastAPI que el token se espera en la cabecera "Authorization" como un Bearer token,
# y que la URL para obtener el token es nuestro endpoint '/api/v1/auth/token'.
# FastAPI usará esto para la documentación de Swagger UI, mostrando un botón "Authorize".
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/token" # La URL completa de tu endpoint de login
)

async def get_current_user(
    db: Session = Depends(get_db), # Inyectamos la sesión de BD
    token: str = Depends(oauth2_scheme) # FastAPI extraerá el token de la cabecera Authorization
) -> models.User: # Esperamos devolver un objeto models.User
    """
    Dependencia para obtener el usuario actual a partir de un token JWT.
    Verifica el token, lo decodifica y obtiene el usuario de la base de datos.
    Lanza HTTPException si el token es inválido, ha expirado o el usuario no se encuentra.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}, # Importante para el estándar OAuth2
    )

    payload = decode_access_token(token) # Usamos nuestra función para decodificar
    if payload is None: # Si decode_access_token retorna None, el token es inválido o expiró
        raise credentials_exception
    
    username: Optional[str] = payload.get("sub") # 'sub' es el claim estándar para el subject (username)
    if username is None:
        raise credentials_exception
    
    # Podríamos validar el payload contra token_schemas.TokenData si quisiéramos más robustez
    # token_data = token_schemas.TokenData(username=username) # Esto validaría que username está presente

    user = user_crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception # Usuario no encontrado en la BD (quizás fue eliminado después de emitir el token)
    
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user) # Esta dependencia llama a la anterior
) -> models.User:
    """
    Dependencia para obtener el usuario actual que también está activo.
    Lanza HTTPException si el usuario está inactivo.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

# Podrías añadir más dependencias aquí si necesitaras roles o permisos más granulares.
# Ejemplo:
# async def get_current_admin_user(
#     current_user: models.User = Depends(get_current_active_user)
# ):
#     if not current_user.is_superuser: # Asumiendo que tu modelo User tiene un campo is_superuser
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
#     return current_user