# app/schemas/user_schemas.py
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# Propiedades base compartidas por todos los schemas de usuario
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único")
    email: Optional[EmailStr] = Field(None, description="Correo electrónico del usuario (opcional, único)")
    # Podríamos añadir más campos como full_name, etc. si fueran necesarios

# Propiedades a recibir al crear un usuario
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Contraseña del usuario (mínimo 8 caracteres)")

# Propiedades a recibir al actualizar un usuario (ejemplo, podría ser más granular)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None)
    is_active: Optional[bool] = Field(None)
    # No permitir actualizar username o password directamente aquí por simplicidad/seguridad.
    # La contraseña tendría su propio endpoint/flujo.

# Propiedades a devolver al cliente (NUNCA la contraseña hasheada)
class User(UserBase): # UserOut o UserInDB también son nombres comunes
    id: int = Field(..., description="ID único del usuario")
    is_active: bool = Field(..., description="Indica si el usuario está activo")

    class Config:
        from_attributes = True