# app/api/v1/category_router.py

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import category_schemas
from app.crud import category_crud
# from app.db import models # Necesario si se usa current_user con tipado models.User
# from app.api import deps # Para cuando se implemente la autenticación

router = APIRouter()

@router.post(
    "/",
    response_model=category_schemas.Category,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva categoría",
    description="Crea una nueva categoría en la base de datos."
)
def create_category_endpoint(
    category_in: category_schemas.CategoryCreate,
    db: Session = Depends(get_db)
    # current_user: models.User = Depends(deps.get_current_active_user) # Descomentar para autenticación
):
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
    summary="Obtener lista de categorías",
    description="Obtiene una lista de todas las categorías, con paginación opcional."
)
def read_categories_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
    # current_user: models.User = Depends(deps.get_current_active_user) # Descomentar para autenticación
):
    categories = category_crud.get_categories(db, skip=skip, limit=limit)
    return categories

@router.get(
    "/{category_id}",
    response_model=category_schemas.Category,
    summary="Obtener una categoría por ID",
    description="Obtiene los detalles de una categoría específica por su ID."
)
def read_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db)
    # current_user: models.User = Depends(deps.get_current_active_user) # Descomentar para autenticación
):
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
    description="Actualiza los detalles de una categoría existente por su ID."
)
def update_category_endpoint(
    category_id: int,
    category_in: category_schemas.CategoryUpdate,
    db: Session = Depends(get_db)
    # current_user: models.User = Depends(deps.get_current_active_user) # Descomentar para autenticación
):
    db_category = category_crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found, cannot update."
        )

    if category_in.name is not None and category_in.name != db_category.name:
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
    response_model=Optional[category_schemas.Category], # Devuelve la categoría eliminada o nada si es 204
    status_code=status.HTTP_200_OK, # O HTTP_204_NO_CONTENT si no se devuelve cuerpo
    summary="Eliminar una categoría",
    description="Elimina una categoría existente por su ID."
)
def delete_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db)
    # current_user: models.User = Depends(deps.get_current_active_user) # Descomentar para autenticación
):
    deleted_category = category_crud.delete_category(db=db, category_id=category_id)
    if deleted_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found, cannot delete."
        )
    # Si quieres un status 204 (No Content), no deberías retornar nada o retornar Response(status_code=204)
    # return None 
    # from fastapi import Response
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    return deleted_category # Devuelve el objeto eliminado con un status 200 OK por defecto