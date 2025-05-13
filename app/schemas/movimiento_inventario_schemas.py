# app/schemas/movimiento_inventario_schemas.py
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

# Importaremos schemas simples para User y Product para evitar importaciones circulares completas
# o definiremos aquí las versiones "Out" que necesitamos.

class UserSimple(BaseModel): # Schema simple para mostrar en Movimiento
    id: int
    username: str
    class Config:
        from_attributes = True

class ProductSimple(BaseModel): # Schema simple para mostrar en Movimiento
    id: int
    name: str
    codigo_sku: Optional[str] = None
    class Config:
        from_attributes = True


class MovimientoInventarioBase(BaseModel):
    producto_id: int = Field(..., description="ID del producto afectado")
    tipo_movimiento: str = Field(..., max_length=50, description="Ej: ENTRADA, SALIDA, AJUSTE")
    cantidad: int = Field(..., gt=0, description="Cantidad del movimiento (siempre positiva)")
    # responsable_id se gestionará internamente a partir del usuario autenticado
    notas: Optional[str] = Field(None, max_length=500)

class MovimientoInventarioCreate(MovimientoInventarioBase):
    pass

# No definimos MovimientoInventarioUpdate por ahora, los movimientos suelen ser inmutables.

class MovimientoInventario(MovimientoInventarioBase):
    id: int
    fecha: datetime
    responsable: Optional[UserSimple] = None # Quién hizo el movimiento
    producto: ProductSimple # Qué producto se movió

    class Config:
        from_attributes = True