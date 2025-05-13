# app/core/config.py
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()

class Settings(BaseSettings):
    # --- Variables de Configuración ---
    PROJECT_NAME: str = "SCL Consulting API"
    API_V1_STR: str = "/api/v1"

    # Base de Datos (leída desde .env)
    # Proporciona un valor por defecto vacío para evitar errores si no está en .env,
    # aunque database.py verificará que no esté vacío antes de usarla.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Configuración JWT (leída desde .env)
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "cambiar_esta_clave_secreta_por_defecto")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Configuración específica de Pydantic v2 (BaseSettings)
    class Config:
        case_sensitive = True # Distingue mayúsculas/minúsculas en las variables de entorno
        env_file = '.env'     # Especifica que se debe cargar el archivo .env (redundante con load_dotenv pero explícito)
        env_file_encoding = 'utf-8'

# Crea una instancia única de la configuración para usar en toda la app
settings = Settings()

# Verificación opcional al inicio (útil para depurar)
# print(f"Database URL loaded: {settings.DATABASE_URL}") # Descomenta temporalmente si tienes problemas