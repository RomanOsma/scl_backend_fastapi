# app/main.py

from fastapi import FastAPI
from app.core.config import settings # Importar la configuración

# --- Importar los routers de la API ---
from app.api.v1 import category_router, product_router # ¡AÑADIDO!
# Más adelante añadiremos:
# from app.api.v1 import product_router
# from app.api.v1 import auth_router
# etc.


# --- Crear la instancia de la aplicación FastAPI ---
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0", # Puedes ajustar la versión según avances
    openapi_url=f"{settings.API_V1_STR}/openapi.json" # Define la ruta para el schema OpenAPI (Swagger)
)

# --- Endpoint Raíz ---
@app.get("/", tags=["Root"])
async def read_root():
    """
    Endpoint raíz que devuelve un mensaje de bienvenida.
    Accesible en la URL base de la API (ej: http://127.0.0.1:8000/).
    """
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

# --- Incluir los routers de la API ---

# Router para las Categorías
app.include_router(
    category_router.router, # El objeto 'router' que definimos en app/api/v1/category_router.py
    prefix=f"{settings.API_V1_STR}/categories", # Todas las rutas de category_router comenzarán con /api/v1/categories
    tags=["Categories"] # Etiqueta para agrupar en la documentación de Swagger
)

# Router para los Productos ¡NUEVO!
app.include_router(
    product_router.router,
    prefix=f"{settings.API_V1_STR}/products",
    tags=["Products"]
)
#
# app.include_router(
# auth_router.router,
# prefix=f"{settings.API_V1_STR}/auth",
# tags=["Authentication"]
# )