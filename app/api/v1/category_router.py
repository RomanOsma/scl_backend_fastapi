# app/api/v1/category_router.py

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import category_schemas
from app.crud import category_crud
from app.db import models # ¡NUEVA IMPORTACIÓN!
from app.api.deps import get_current_active_user # ¡NUEVA IMPORTACIÓN!

router = APIRouter()

@router.post(
    "/",
    response_model=category_schemas.Category,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva categoría",
    description="Crea una nueva categoría en la base de datos. Requiere autenticación." # Añadido
)
def create_category_endpoint(
    category_in: category_schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user) # ¡AÑADIDO!
):
    # ... (lógica existente para crear categoría) ...
    db_category_by_name = category_crud.get_category_by_name(db, name=category_in.name)
    if db_category_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name '{category_in.name}' already exists."
        )
    created_category = category_crud.create_category(db=db, category=category_in)
    return created_category

@router.get(
    "/",
    response_model=List[category_schemas.Category],
    summary="Obtener lista de categorías"
    # No protegemos el listado por ahora
)
def read_categories_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    # ... (lógica existente) ...
    categories = category_crud.get_categories(db, skip=skip, limit=limit)
    return categories


@router.get(
    "/{category_id}",
    response_model=category_schemas.Category,
    summary="Obtener una categoría por ID"
    # No protegemos la lectura individual por ahora
)
def read_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db)
):
    # ... (lógica existente) ...
    db_category = category_crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found"
        )
    return db_category


@router.put(
    "/{category_id}",
    response_model=category_schemas.Category,
    summary="Actualizar una categoría existente",
    description="Actualiza los detalles de una categoría existente. Requiere autenticación." # Añadido
)
def update_category_endpoint(
    category_id: int,
    category_in: category_schemas.CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user) # ¡AÑADIDO!
):
    # ... (lógica existente para actualizar categoría, incluyendo verificaciones) ...
    db_category_to_update = category_crud.get_category(db, category_id=category_id) # Renombrado para claridad
    if db_category_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found, cannot update."
        )

    if category_in.name is not None and category_in.name != db_category_to_update.name:
        existing_category_with_new_name = category_crud.get_category_by_name(db, name=category_in.name)
        if existing_category_with_new_name and existing_category_with_new_name.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Another category with name '{category_in.name}' already exists."
            )
            
    updated_category = category_crud.update_category(db=db, category_id=category_id, category_update=category_in)
    return updated_category


@router.delete(
    "/{category_id}",
    response_model=Optional[category_schemas.Category],
    status_code=status.HTTP_200_OK,
    summary="Eliminar una categoría",
    description="Elimina una categoría existente. Requiere autenticación." # Añadido
)
def delete_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user) # ¡AÑADIDO!
):
    # ... (lógica existente para eliminar categoría) ...
    deleted_category = category_crud.delete_category(db=db, category_id=category_id)
    if deleted_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found, cannot delete."
        )
    return deleted_category