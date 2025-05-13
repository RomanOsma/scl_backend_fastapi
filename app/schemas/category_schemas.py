# app/schemas/category_schemas.py

from typing import Optional
from pydantic import BaseModel, Field # Field para validaciones extra si son necesarias

# --- Propiedades Base ---
# Estas son las propiedades comunes que pueden estar presentes al crear o leer una categoría.
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Nombre de la categoría")
    description: Optional[str] = Field(None, max_length=500, description="Descripción opcional de la categoría")

# --- Propiedades para la Creación ---
# Hereda de CategoryBase. Estas son las propiedades que se esperan al crear una nueva categoría.
# No necesitamos campos adicionales a los de CategoryBase para la creación por ahora.
class CategoryCreate(CategoryBase):
    pass # No se necesitan campos adicionales a los de CategoryBase para la creación

# --- Propiedades para la Actualización ---
# Todos los campos son opcionales al actualizar.
# Un cliente podría querer actualizar solo el nombre, solo la descripción, o ambos.
class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100, description="Nuevo nombre de la categoría (opcional)")
    description: Optional[str] = Field(None, max_length=500, description="Nueva descripción de la categoría (opcional)")

# --- Propiedades para la Respuesta (al leer desde la BD) ---
# Este es el modelo que se devolverá al cliente.
# Hereda de CategoryBase e incluye el 'id' y cualquier otro campo que se genere en la BD
# o que solo deba ser visible en las respuestas.
class Category(CategoryBase):
    id: int = Field(..., description="Identificador único de la categoría")

    # Configuración para Pydantic v1: orm_mode = True
    # Configuración para Pydantic v2: from_attributes = True
    # Esto permite que Pydantic cree el modelo a partir de un objeto ORM (SQLAlchemy).
    class Config:
        from_attributes = True