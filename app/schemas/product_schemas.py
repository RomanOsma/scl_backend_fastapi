# app/schemas/product_schemas.py

from typing import Optional, List
from pydantic import BaseModel, Field

# Importamos el schema de Category para usarlo en la respuesta de Product
from .category_schemas import Category as CategorySchema

# --- Propiedades Base del Producto ---
class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=200, description="Nombre del producto")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción detallada del producto")
    price: float = Field(..., gt=0, description="Precio del producto, debe ser mayor que cero") # gt = greater than
    stock_actual: int = Field(default=0, ge=0, description="Cantidad actual en stock") # ge = greater than or equal to
    stock_minimo: int = Field(default=0, ge=0, description="Nivel mínimo de stock antes de alerta")
    codigo_sku: Optional[str] = Field(None, max_length=100, description="Código SKU único del producto (opcional)")
    numero_serie: Optional[str] = Field(None, max_length=100, description="Número de serie único (si aplica, opcional)")
    
    # category_id es opcional al crear/actualizar si un producto puede no tener categoría
    category_id: Optional[int] = Field(None, description="ID de la categoría a la que pertenece el producto (opcional)")

# --- Propiedades para la Creación de un Producto ---
# Hereda de ProductBase. Todos los campos de ProductBase son necesarios o tienen default.
class ProductCreate(ProductBase):
    pass

# --- Propiedades para la Actualización de un Producto ---
# Todos los campos son opcionales al actualizar.
class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    stock_actual: Optional[int] = Field(None, ge=0)
    stock_minimo: Optional[int] = Field(None, ge=0)
    codigo_sku: Optional[str] = Field(None, max_length=100)
    numero_serie: Optional[str] = Field(None, max_length=100)
    category_id: Optional[int] = Field(None) # Permite cambiar o quitar la categoría

# --- Propiedades para la Respuesta (al leer desde la BD) ---
# Este es el modelo que se devolverá al cliente.
class Product(ProductBase):
    id: int = Field(..., description="Identificador único del producto")
    
    # Aquí anidamos la información de la categoría
    # Usamos el schema 'CategorySchema' que importamos
    category: Optional[CategorySchema] = Field(None, description="Categoría asociada al producto")

    class Config:
        from_attributes = True # Permite crear desde objetos ORM