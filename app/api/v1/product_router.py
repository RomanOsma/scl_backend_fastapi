# app/api/v1/product_router.py

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import product_schemas
from app.crud import product_crud, category_crud
from app.db import models # ¡NUEVA IMPORTACIÓN!
from app.api.deps import get_current_active_user # ¡NUEVA IMPORTACIÓN!

router = APIRouter()

@router.post(
    "/",
    response_model=product_schemas.Product,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo producto",
    description="Crea un nuevo producto. Requiere autenticación." # Añadido
)
def create_product_endpoint(
    product_in: product_schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user) # ¡AÑADIDO!
):
    # ... (lógica existente para crear producto) ...
    if product_in.category_id is not None:
        category = category_crud.get_category(db, category_id=product_in.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {product_in.category_id} not found. Cannot create product."
            )
    
    if product_in.codigo_sku:
        existing_product_by_sku = product_crud.get_product_by_sku(db, sku=product_in.codigo_sku)
        if existing_product_by_sku:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with SKU '{product_in.codigo_sku}' already exists."
            )
            
    created_product = product_crud.create_product(db=db, product=product_in)
    return created_product


@router.get(
    "/",
    response_model=List[product_schemas.Product],
    summary="Obtener lista de productos"
    # No protegemos el listado por ahora
)
def read_products_endpoint(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = Query(None, description="Filtrar productos por ID de categoría"),
    db: Session = Depends(get_db)
):
    # ... (lógica existente) ...
    products = product_crud.get_products(db, skip=skip, limit=limit, category_id=category_id)
    return products


@router.get(
    "/{product_id}",
    response_model=product_schemas.Product,
    summary="Obtener un producto por ID"
    # No protegemos la lectura individual por ahora
)
def read_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db)
):
    # ... (lógica existente) ...
    db_product = product_crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return db_product


@router.put(
    "/{product_id}",
    response_model=product_schemas.Product,
    summary="Actualizar un producto existente",
    description="Actualiza un producto existente. Requiere autenticación." # Añadido
)
def update_product_endpoint(
    product_id: int,
    product_in: product_schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user) # ¡AÑADIDO!
):
    # ... (lógica existente para actualizar producto, incluyendo verificaciones) ...
    db_product_to_update = product_crud.get_product(db, product_id=product_id)
    if db_product_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found, cannot update."
        )

    if product_in.category_id is not None and product_in.category_id != db_product_to_update.category_id:
        category = category_crud.get_category(db, category_id=product_in.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"New category with ID {product_in.category_id} not found. Cannot update product."
            )

    if product_in.codigo_sku is not None and product_in.codigo_sku != db_product_to_update.codigo_sku:
        existing_product_by_sku = product_crud.get_product_by_sku(db, sku=product_in.codigo_sku)
        if existing_product_by_sku and existing_product_by_sku.id != product_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Another product with SKU '{product_in.codigo_sku}' already exists."
            )
            
    updated_product = product_crud.update_product(db=db, product_id=product_id, product_update=product_in)
    return updated_product

@router.delete(
    "/{product_id}",
    response_model=Optional[product_schemas.Product],
    status_code=status.HTTP_200_OK,
    summary="Eliminar un producto",
    description="Elimina un producto existente. Requiere autenticación." # Añadido
)
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user) # ¡AÑADIDO!
):
    # ... (lógica existente para eliminar producto) ...
    deleted_product = product_crud.delete_product(db=db, product_id=product_id)
    if deleted_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found, cannot delete."
        )
    return deleted_product