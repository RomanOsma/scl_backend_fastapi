# app/crud/user_crud.py

from typing import Optional
from sqlalchemy.orm import Session

from app.db import models # Importamos nuestros modelos SQLAlchemy (models.User)
from app.schemas import user_schemas # Importamos nuestros schemas Pydantic para usuarios
from app.security.auth_security import get_password_hash, verify_password # Funciones de hashing

# --- Operaciones de Lectura (Read) ---

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """
    Obtiene un usuario específico por su ID.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    Obtiene un usuario específico por su correo electrónico.
    """
    if not email: # No buscar si email es None o vacío
        return None
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """
    Obtiene un usuario específico por su nombre de usuario.
    """
    return db.query(models.User).filter(models.User.username == username).first()

# --- Operación de Creación (Create) ---

def create_user(db: Session, user: user_schemas.UserCreate) -> models.User:
    """
    Crea un nuevo usuario en la base de datos.
    La contraseña se hashea antes de guardarla.
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=True # Por defecto, los usuarios se crean activos
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Operación de Autenticación (No es CRUD puro, pero va aquí por lógica) ---

def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    """
    Autentica a un usuario.
    Busca al usuario por nombre de usuario y verifica su contraseña.

    :param db: Sesión de la base de datos.
    :param username: Nombre de usuario.
    :param password: Contraseña en texto plano.
    :return: El objeto User si la autenticación es exitosa, sino None.
    """
    user = get_user_by_username(db, username=username)
    if not user:
        return None # Usuario no encontrado
    if not verify_password(password, user.hashed_password):
        return None # Contraseña incorrecta
    
    # Podríamos añadir una verificación de user.is_active aquí si quisiéramos
    # if not user.is_active:
    #     return None # Usuario inactivo

    return user

# --- Operaciones de Actualización (Update) - Ejemplo Básico ---
# Podríamos expandir esto significativamente si es necesario

def update_user_activity(db: Session, user_id: int, is_active: bool) -> Optional[models.User]:
    """
    Actualiza el estado 'is_active' de un usuario.
    """
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        return None
    
    db_user.is_active = is_active
    db.add(db_user) # Opcional para objetos ya rastreados si solo modificas, pero buena práctica
    db.commit()
    db.refresh(db_user)
    return db_user

# Podríamos añadir funciones para actualizar email, contraseña (con más seguridad), etc.