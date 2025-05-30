# SCL Inventory - Wiki

https://deepwiki.com/RomanOsma/scl_backend_fastapi

# SCL Inventory - Backend API (FastAPI)

Backend API para el sistema de gestión de inventario SCL, desarrollado con FastAPI, SQLAlchemy y Pydantic, utilizando PostgreSQL como base de datos (preparado para Supabase).

## Ejecución Local

### Prerrequisitos
*   Python 3.10 o superior
*   pip (gestor de paquetes de Python)
*   Git
*   Una instancia de PostgreSQL accesible (ej. local o una cuenta gratuita en Supabase).

### Pasos

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/RomanOsma/scl_backend_fastapi.git
    cd scl_backend_fastapi
    ```

2.  **Crear y Activar Entorno Virtual:**
    Se recomienda encarecidamente usar un entorno virtual.
    ```bash
    python -m venv venv
    ```
    Activación:
    *   Windows (CMD): `venv\Scripts\activate.bat`
    *   Windows (PowerShell): `venv\Scripts\Activate.ps1` (puede requerir cambiar la política de ejecución: `Set-ExecutionPolicy Unrestricted -Scope Process`)
    *   macOS/Linux (bash/zsh): `source venv/bin/activate`

3.  **Instalar Dependencias:**
    Con el entorno virtual activado:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno:**
    *   Crea un archivo llamado `.env` en la raíz del proyecto (`scl_backend_fastapi/.env`).
    *   Añade el siguiente contenido, reemplazando los placeholders con tus valores reales:
        ```env
        # scl_backend_fastapi/.env

        # Ejemplo para Supabase (reemplaza con tus datos):
        # DATABASE_URL=postgresql://postgres:[TU_CONTRASENA_SUPABASE]@[TU_PROYECTO_REF].db.supabase.co:5432/postgres
        # Ejemplo para PostgreSQL local:
        # DATABASE_URL=postgresql://tu_usuario_pg:tu_contrasena_pg@localhost:5432/tu_base_de_datos_pg
        DATABASE_URL=TU_CADENA_DE_CONEXION_POSTGRESQL_COMPLETA

        # Genera una clave fuerte y aleatoria (ej. usando `openssl rand -hex 32`)
        JWT_SECRET_KEY=UNA_CLAVE_SECRETA_MUY_LARGA_ALEATORIA_Y_SEGURA_PARA_JWT
        ALGORITHM=HS256
        ACCESS_TOKEN_EXPIRE_MINUTES=60

        # Orígenes permitidos para CORS (para desarrollo local con el frontend en puerto 8001)
        BACKEND_CORS_ORIGINS=http://127.0.0.1:8001,http://localhost:8001
        ```

5.  **Aplicar Migraciones de Base de Datos (Alembic):**
    Asegúrate de que tu `DATABASE_URL` en `.env` es correcta y la base de datos está accesible.
    ```bash
    alembic upgrade head
    ```
    Esto creará todas las tablas necesarias en tu base de datos.

6.  **(Opcional) Poblar la Base de Datos con Datos de Ejemplo:**
    Si el script `seed_db.py` está presente y configurado:
    ```bash
    python seed_db.py
    ```

7.  **Ejecutar el Servidor FastAPI:**
    ```bash
    uvicorn app.main:app --reload --port 8000
    ```

8.  **Acceder a la API:**
    *   La API estará disponible en `http://127.0.0.1:8000`.
    *   La documentación interactiva (Swagger UI) estará en: `http://127.0.0.1:8000/docs`
    *   Un endpoint de estado (health check) está en: `http://127.0.0.1:8000/health`
