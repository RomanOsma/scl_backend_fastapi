# app/schemas/proveedor_schemas.py
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr

# Reutilizaremos Product schema sin su categoría para evitar importación circular
# o definiremos un ProductSimple para las listas de productos de un proveedor.
# Por ahora, no lo incluimos en la respuesta de Proveedor para simplificar.

class ProveedorBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    contacto_nombre: Optional[str] = Field(None, max_length=100)
    contacto_email: Optional[EmailStr] = Field(None)
    contacto_telefono: Optional[str] = Field(None, max_length=30)
    direccion: Optional[str] = Field(None, max_length=500)

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=150)
    contacto_nombre: Optional[str] = Field(None, max_length=100)
    contacto_email: Optional[EmailStr] = Field(None)
    contacto_telefono: Optional[str] = Field(None, max_length=30)
    direccion: Optional[str] = Field(None, max_length=500)

class Proveedor(ProveedorBase):
    id: int
    # products: List[ProductSimpleSchema] = [] # Para más adelante si queremos mostrar productos

    class Config:
        from_attributes = True