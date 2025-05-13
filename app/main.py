# app/main.py

from fastapi import FastAPI  # <--- ¡IMPORTANTE! Importar FastAPI
from app.core.config import settings # Importar la configuración

# --- Crear la instancia de la aplicación FastAPI ---
# Esta variable 'app' es la que usan los decoradores @app.get, @app.post, etc.
app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0") # <--- ¡IMPORTANTE! Crear la instancia 'app'

# --- Endpoint Raíz ---
@app.get("/", tags=["Root"]) # Ahora este decorador encontrará la variable 'app'
async def read_root():
    """
    Endpoint raíz que devuelve un mensaje de bienvenida.
    """
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

# --- Inclusión de Routers (se añadirán más adelante) ---
# from app.api.v1 import category_router, product_router # etc.
#
# app.include_router(category_router.router, prefix=f"{settings.API_V1_STR}/categories", tags=["Categories"])
# app.include_router(product_router.router, prefix=f"{settings.API_V1_STR}/products", tags=["Products"])
# ... más routers