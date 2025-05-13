# alembic/env.py

# --- INICIO: Añadir directorio raíz del proyecto a sys.path ---
import os
import sys
alembic_dir = os.path.dirname(__file__)
project_root = os.path.dirname(alembic_dir)
sys.path.insert(0, project_root)
# --- FIN: Añadir directorio raíz del proyecto a sys.path ---

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# --- INICIO: Importar Base, settings Y TUS MODELOS ---
from app.db.database import Base
from app.core.config import settings
import app.db.models  # <--- ¡AÑADE ESTA LÍNEA IMPORTANTE!
                      # Esto asegura que las clases User, Category, Product se definan
                      # y se registren con la Base antes de que usemos Base.metadata.
# --- FIN: Importar Base, settings Y TUS MODELOS ---

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- INICIO: Establecer target_metadata ---
target_metadata = Base.metadata
print("Base metadata tables (después de importar models):", Base.metadata.tables.keys()) # Mantenemos el print para verificar
# --- FIN: Establecer target_metadata ---

# ... (el resto del archivo env.py permanece igual) ...
def run_migrations_offline() -> None:
    # ... (código como antes) ...
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    # ... (código como antes) ...
    ini_section = config.get_section(config.config_ini_section, {})
    ini_section['sqlalchemy.url'] = settings.DATABASE_URL
    connectable = engine_from_config(
        ini_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()