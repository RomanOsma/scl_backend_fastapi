# app/api/v1/auth_router.py

from datetime import timedelta
from typing import Any # Any se usa a veces para form_data, pero se puede ser más explícito

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # Para el formulario de login estándar
from sqlalchemy.orm import Session

from app.core.config import settings # Para ACCESS_TOKEN_EXPIRE_MINUTES
from app.db.database import get_db
from app.schemas import token_schemas, user_schemas # Schemas para Token y User
from app.crud import user_crud # Funciones CRUD y de autenticación de usuario
from app.security.auth_security import create_access_token # Para crear el JWT
from app.db import models

router = APIRouter()

@router.post(
    "/token", # Ruta estándar OAuth2 para obtener un token (también común: "/login" o "/login/access-token")
    response_model=token_schemas.Token,
    summary="Obtener Token de Acceso (Login)",
    description="Autentica a un usuario con nombre de usuario y contraseña, y devuelve un token de acceso JWT."
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), # Espera datos de formulario (username, password)
    db: Session = Depends(get_db)
) -> token_schemas.Token: # Especificamos que la función retorna un objeto Token
    """
    Endpoint de login.
    Recibe `username` y `password` como datos de formulario.
    """
    user = user_crud.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}, # Estándar para errores de autenticación Bearer
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, # O 403 Forbidden
            detail="Usuario inactivo"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id}, # 'sub' (subject) es el claim estándar para el identificador del usuario
        expires_delta=access_token_expires
    )
    return token_schemas.Token(access_token=access_token, token_type="bearer")


# --- [OPCIONAL] Endpoint de Registro de Usuario ---
# Si quieres permitir el registro directamente desde la API.
# La "Prueba Técnica SCL" menciona "sistema de login tradicional", lo que podría implicar
# que el registro se maneja de otra forma o a través del frontend Django directamente.
# Si el frontend Django ya tiene un sistema de usuarios, este endpoint de registro API
# podría no ser necesario o podría ser para otro tipo de usuarios (ej: usuarios API).

@router.post(
    "/register",
    response_model=user_schemas.User,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario (Opcional)",
    description="Crea una nueva cuenta de usuario. Verificar si este endpoint es requerido por el proyecto."
)
def register_new_user(
    user_in: user_schemas.UserCreate,
    db: Session = Depends(get_db)
) -> models.User: # Ahora 'models' está definido
    # ... (lógica de la función) ...
    db_user_by_username = user_crud.get_user_by_username(db, username=user_in.username)
    if db_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El nombre de usuario '{user_in.username}' ya está registrado."
        )
    
    if user_in.email:
        db_user_by_email = user_crud.get_user_by_email(db, email=user_in.email)
        if db_user_by_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El correo electrónico '{user_in.email}' ya está registrado."
            )
            
    created_user = user_crud.create_user(db=db, user=user_in)
    return created_user