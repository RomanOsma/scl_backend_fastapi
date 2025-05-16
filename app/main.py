# scl_backend_fastapi/app/main.py

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings

# --- Importar los routers individuales directamente ---
from app.api.v1 import auth_router
from app.api.v1 import category_router
from app.api.v1 import product_router
from app.api.v1 import proveedor_router
from app.api.v1 import movimiento_inventario_router
# Asegúrate de que los nombres de archivo de tus routers coincidan
# y que cada uno de esos archivos tenga una variable 'router = APIRouter()'

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# --- Configuración de CORS ---
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# --- Endpoint Raíz que Redirige a /docs ---
@app.get("/", include_in_schema=False)
async def root_redirect_to_docs():
    return RedirectResponse(url="/docs")

# --- Endpoint de Health Check ---
@app.get("/health", tags=["Utilities"], summary="Verifica el estado de la API")
async def health_check():
    return {"status": "ok", "message": f"Welcome to {settings.PROJECT_NAME}!"}


# --- Incluir los routers de la API ---
# Cada router se incluye con su prefijo y tags
app.include_router(
    auth_router.router, 
    prefix=f"{settings.API_V1_STR}/auth", 
    tags=["Authentication"]
)
app.include_router(
    category_router.router, 
    prefix=f"{settings.API_V1_STR}/categories", 
    tags=["Categories"]
)
app.include_router(
    product_router.router, 
    prefix=f"{settings.API_V1_STR}/products", 
    tags=["Products"]
)
app.include_router(
    proveedor_router.router, 
    prefix=f"{settings.API_V1_STR}/proveedores", 
    tags=["Proveedores"]
)
app.include_router(
    movimiento_inventario_router.router, 
    prefix=f"{settings.API_V1_STR}/movimientos", 
    tags=["Movimientos de Inventario"]
)

# Ejemplo de evento de startup (opcional)
@app.on_event("startup")
async def startup_event():
    print(f"INFO (backend main.py): Aplicación FastAPI {settings.PROJECT_NAME} v{settings.PROJECT_VERSION} iniciada y lista.")