# app/api/v1/movimiento_inventario_router.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import movimiento_inventario_schemas
from app.crud import movimiento_inventario_crud, product_crud # Necesario para validar producto
from app.db import models
from app.api.deps import get_current_active_user

router = APIRouter()

@router.post(
    "/",
    response_model=movimiento_inventario_schemas.MovimientoInventario,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo movimiento de inventario",
)
def create_new_movimiento(
    movimiento_in: movimiento_inventario_schemas.MovimientoInventarioCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    # Validar que el producto existe antes de llamar al CRUD
    # (Aunque el CRUD también lo valida, es bueno tenerlo aquí para un error HTTP más claro)
    db_producto = product_crud.get_product(db, product_id=movimiento_in.producto_id) # Corregido
    if not db_producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {movimiento_in.producto_id} no encontrado. No se puede crear movimiento."
        )
    try:
        return movimiento_inventario_crud.create_movimiento_inventario(
            db=db, movimiento=movimiento_in, responsable_id=current_user.id
        )
    except ValueError as e: # Captura errores de lógica de negocio del CRUD
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/producto/{producto_id}",
    response_model=List[movimiento_inventario_schemas.MovimientoInventario],
    summary="Obtener movimientos de inventario para un producto específico",
)
def read_movimientos_for_product(
    producto_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(get_current_active_user), # Opcional proteger este listado
):
    # Validar que el producto existe
    db_producto = product_crud.get_product(db, product_id=producto_id) # Corregido
    if not db_producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado."
        )
    return movimiento_inventario_crud.get_movimientos_por_producto(
        db, producto_id=producto_id, skip=skip, limit=limit
    )

# GET individual y DELETE para movimientos suelen ser menos comunes o tener lógica de negocio especial.
# Por ahora, nos centramos en crear y listar por producto.