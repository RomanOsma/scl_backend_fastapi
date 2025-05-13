# app/crud/movimiento_inventario_crud.py
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func # Para sumas y lógica de stock

from app.db import models
from app.schemas import movimiento_inventario_schemas
from app.crud import product_crud # Para actualizar el stock del producto

def get_movimiento(db: Session, movimiento_id: int) -> Optional[models.MovimientoInventario]:
    return (
        db.query(models.MovimientoInventario)
        .options(
            joinedload(models.MovimientoInventario.producto),
            joinedload(models.MovimientoInventario.responsable)
        )
        .filter(models.MovimientoInventario.id == movimiento_id)
        .first()
    )

def get_movimientos_por_producto(
    db: Session, producto_id: int, skip: int = 0, limit: int = 100
) -> List[models.MovimientoInventario]:
    return (
        db.query(models.MovimientoInventario)
        .options(
            joinedload(models.MovimientoInventario.producto),
            joinedload(models.MovimientoInventario.responsable)
        )
        .filter(models.MovimientoInventario.producto_id == producto_id)
        .order_by(models.MovimientoInventario.fecha.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_movimiento_inventario(
    db: Session,
    movimiento: movimiento_inventario_schemas.MovimientoInventarioCreate,
    responsable_id: int
) -> models.MovimientoInventario:
    # 1. Validar que el producto exista
    db_producto = product_crud.get_product(db, producto_id=movimiento.producto_id)
    if not db_producto:
        # Esta validación debería estar en el router para lanzar HTTPException
        # Aquí simplemente no procedemos o podríamos lanzar un ValueError
        raise ValueError(f"Producto con ID {movimiento.producto_id} no encontrado.")

    # 2. Crear el movimiento
    db_movimiento = models.MovimientoInventario(
        **movimiento.model_dump(),
        responsable_id=responsable_id
        # fecha se establece por server_default si no se pasa
    )
    db.add(db_movimiento)
    
    # 3. Actualizar el stock del producto
    # Es crucial que esto sea atómico con la creación del movimiento (dentro de la misma transacción)
    cantidad_a_ajustar = 0
    if movimiento.tipo_movimiento.upper() in ["ENTRADA", "AJUSTE_POSITIVO", "AJUSTE_INICIAL"]:
        cantidad_a_ajustar = movimiento.cantidad
    elif movimiento.tipo_movimiento.upper() in ["SALIDA", "AJUSTE_NEGATIVO"]:
        cantidad_a_ajustar = -movimiento.cantidad
    else:
        # Tipo de movimiento no reconocido, no ajustar stock o lanzar error
        # Por ahora, no ajustamos si el tipo no es conocido.
        pass 
        # Opcional: raise ValueError(f"Tipo de movimiento '{movimiento.tipo_movimiento}' no reconocido para ajuste de stock.")


    if cantidad_a_ajustar != 0:
        db_producto.stock_actual = (db_producto.stock_actual or 0) + cantidad_a_ajustar
        db.add(db_producto) # Marcar el producto como modificado

    db.commit()
    db.refresh(db_movimiento)
    # Para que las relaciones se carguen:
    return get_movimiento(db, movimiento_id=db_movimiento.id)