# app/schemas/token_schemas.py
from typing import Optional
from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer") # El tipo de token, usualmente "bearer"

class TokenData(BaseModel):
    # Contenido del payload del JWT que nos interesa
    username: Optional[str] = Field(None)
    # Podríamos añadir 'user_id' o 'scopes' (permisos) aquí si fuera necesario