# scl_backend_fastapi/app/core/config.py
import os
from typing import List, Optional, Union, Any # <--- AÑADE 'Union' AQUÍ
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pydantic import field_validator

# ... (el resto del archivo config.py que te pasé antes se mantiene igual) ...
# Solo asegúrate de que la línea de importación de 'typing' arriba sea la correcta.

# Determinar la ruta al archivo .env en la raíz del proyecto backend
BASE_DIR_CONFIG = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(BASE_DIR_CONFIG, '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"ADVERTENCIA (backend config): No se encontró el archivo .env en {dotenv_path}. Las variables deben estar en el entorno.")


class Settings(BaseSettings):
    PROJECT_NAME: str = "SCL Inventory API"
    PROJECT_VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256" 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 

    BACKEND_CORS_ORIGINS: Optional[Union[str, List[str]]] = None

    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    @classmethod
    def assemble_cors_origins(cls, v: Optional[str]) -> List[str]:
        if isinstance(v, str) and v:
            return [origin.strip() for origin in v.split(',')]
        if isinstance(v, list):
            return v
        return [] 

    model_config = SettingsConfigDict(
        env_file=dotenv_path if os.path.exists(dotenv_path) else None,
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )

settings = Settings()

if not settings.BACKEND_CORS_ORIGINS:
    print("ADVERTENCIA (backend config): BACKEND_CORS_ORIGINS no tiene valores configurados. CORS podría no funcionar como se espera.")
else:
    print(f"INFO (backend config): BACKEND_CORS_ORIGINS configurado para: {settings.BACKEND_CORS_ORIGINS}")