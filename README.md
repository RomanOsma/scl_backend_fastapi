# SCL Inventory - Backend API (FastAPI)

Backend API para el sistema de gestión de inventario SCL.

## Ejecución Local

### Prerrequisitos
*   Python 3.10+
*   pip
*   Git
*   Acceso a una base de datos PostgreSQL (configurada en `.env`)

### Pasos

1.  **Clonar el Repositorio (si aún no lo has hecho):**
    ```bash
    git clone https://github.com/RomanOsma/scl_backend_fastapi.git
    cd scl_backend_fastapi
    ```

2.  **Crear y Activar Entorno Virtual:**
    ```bash
    python -m venv venv
    # Windows CMD:
    venv\Scripts\activate.bat
    # Windows PowerShell:
    # venv\Scripts\Activate.ps1
    # macOS/Linux:
    # source venv/bin/activate
    ```

3.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno:**
    *   Crea un archivo `.env` en la raíz del proyecto (`scl_backend_fastapi/.env`).
    *   Añade las siguientes variables con tus valores:
        ```env
        DATABASE_URL=postgresql://postgres:[TU_PASSWORD_SUPABASE]@[TU_HOST_SUPABASE]:[PUERTO_SUPABASE]/postgres
        JWT_SECRET_KEY=UNA_CLAVE_SECRETA_MUY_LARGA_Y_ALEATORIA
        ALGORITHM=HS256
        ACCESS_TOKEN_EXPIRE_MINUTES=30
        # Opcional: Para permitir peticiones del frontend local
        BACKEND_CORS_ORIGINS=http://127.0.0.1:8001,http://localhost:8001
        ```
    *   **Importante:** Reemplaza los placeholders (`[...]`) con tus datos reales.

5.  **Aplicar Migraciones de Base de Datos:**
    (Asegúrate de que `DATABASE_URL` en `.env` es correcta)
    ```bash
    alembic upgrade head
    ```

6.  **(Opcional) Poblar Base de Datos:**
    ```bash
    python seed_db.py
    ```

7.  **Ejecutar Servidor FastAPI:**
    (Asegúrate de que el comando `app.main:app` coincide con tu estructura de proyecto. Si `main.py` está en la raíz, usa `main:app`)
    ```bash
    uvicorn app.main:app --reload --port 8000
    ```

8.  **Acceder a la API:**
    *   La API estará disponible en `http://127.0.0.1:8000`.
    *   Documentación (Swagger UI): `http://127.0.0.1:8000/docs`
    *   Health Check: `http://127.0.0.1:8000/health`