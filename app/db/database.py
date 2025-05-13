# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings # Importa la configuración

# --- Verificación Crucial ---
# Asegurarse de que la URL de la base de datos se cargó correctamente desde .env
if not settings.DATABASE_URL or settings.DATABASE_URL == "":
    print("ERROR FATAL: La variable de entorno DATABASE_URL no está configurada o está vacía.")
    print("Asegúrate de que el archivo .env existe en la raíz del backend y contiene la línea DATABASE_URL=...")
    # Podrías lanzar una excepción aquí para detener la ejecución si prefieres:
    # raise ValueError("DATABASE_URL environment variable not set or empty")
    # Por ahora, solo imprimimos el error. El create_engine fallará después si está vacía.

# --- Configuración de SQLAlchemy ---

# Crea el motor de SQLAlchemy usando la URL del pooler leída desde settings
# Ejemplo URL Pooler: postgresql://<user.project_ref>:<password>@<pooler_host>:<port>/<db>
engine = create_engine(
    settings.DATABASE_URL,
    # pool_pre_ping=True # Opcional: verifica conexión antes de usarla del pool
    # pool_size=10       # Opcional: tamaño del pool (ajustar según necesidad)
    # max_overflow=20    # Opcional: conexiones temporales extra
)

# Crea una fábrica de sesiones configurada para usar el motor
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea una clase Base para que nuestros modelos ORM hereden de ella
Base = declarative_base()

# --- Dependencia para FastAPI ---
# Función para obtener una sesión de base de datos en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db # Proporciona la sesión al endpoint
    finally:
        db.close() # Asegura que la sesión se cierre después de usarla