# app/crud/category_crud.py

from typing import List, Optional
from sqlalchemy.orm import Session

from app.db import models
from app.schemas import category_schemas

# --- Operaciones de Lectura (Read) ---

def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    """
    Obtiene una categoría específica por su ID.
    Retorna el objeto Category o None si no se encuentra.
    """
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_name(db: Session, name: str) -> Optional[models.Category]:
    """
    Obtiene una categoría específica por su nombre.
    Retorna el objeto Category o None si no se encuentra.
    (Útil para evitar duplicados por nombre).
    """
    return db.query(models.Category).filter(models.Category.name == name).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    """
    Obtiene una lista de categorías, con paginación opcional.
    Retorna una lista de objetos Category.
    """
    return db.query(models.Category).offset(skip).limit(limit).all()

# --- Operación de Creación (Create) ---

def create_category(db: Session, category: category_schemas.CategoryCreate) -> models.Category:
    """
    Crea una nueva categoría en la base de datos.
    Retorna el objeto Category recién creado.
    """
    db_category = models.Category(
        name=category.name,
        description=category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# --- Operación de Actualización (Update) ---

def update_category(
    db: Session,
    category_id: int,
    category_update: category_schemas.CategoryUpdate
) -> Optional[models.Category]:
    """
    Actualiza una categoría existente.
    Retorna el objeto Category actualizado o None si no se encuentra.
    """
    db_category = get_category(db, category_id=category_id)
    if not db_category:
        return None

    # Obtiene los datos del schema de Pydantic como un diccionario,
    # excluyendo los campos que no se establecieron (None por defecto en el schema Update)
    # o que no se enviaron en la solicitud.
    update_data = category_update.model_dump(exclude_unset=True) # Para Pydantic v2
    # Si usaras Pydantic v1, sería: update_data = category_update.dict(exclude_unset=True)


    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.add(db_category) # SQLAlchemy es lo suficientemente inteligente para saber si es un INSERT o UPDATE
    db.commit()
    db.refresh(db_category)
    return db_category

# --- Operación de Eliminación (Delete) ---

def delete_category(db: Session, category_id: int) -> Optional[models.Category]:
    """
    Elimina una categoría existente.
    Retorna el objeto Category eliminado o None si no se encuentra.
    (Podrías también retornar solo un booleano o el id si la eliminación fue exitosa).
    """
    db_category = get_category(db, category_id=category_id)
    if not db_category:
        return None

    db.delete(db_category)
    db.commit()
    return db_category # El objeto aún contiene los datos de lo que fue eliminado