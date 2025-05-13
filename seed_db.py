# scl_backend_fastapi/seed_db.py

import sys
import os

# --- INICIO: Configuración de sys.path para importaciones ---
# Ruta absoluta al directorio donde está este script (scl_backend_fastapi/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Si el script está en la raíz del proyecto backend, y 'app' es un subdirectorio,
# añadimos la raíz del proyecto para que 'app.modulo' funcione.
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
# --- FIN: Configuración de sys.path ---

# Ahora las importaciones deberían funcionar
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base # Importamos SessionLocal, engine y Base
from app.db import models # Importamos todos nuestros modelos
from app.security.auth_security import get_password_hash # Para hashear la contraseña del usuario

# --- Crear todas las tablas (si no existen) ---
# Esto es útil si ejecutas el seed en una BD limpia sin haber corrido migraciones de Alembic antes.
# Si ya corriste Alembic, estas tablas ya deberían existir y esto no hará nada.
print("Intentando crear tablas si no existen (Alembic ya debería haberlas creado)...")
try:
    Base.metadata.create_all(bind=engine)
    print("Verificación/creación de tablas completada.")
except Exception as e:
    print(f"Error durante Base.metadata.create_all: {e}")
    print("Asegúrate de que la conexión a la base de datos esté configurada correctamente en .env")
    sys.exit(1) # Salir si no se pueden crear/verificar las tablas


def seed_data():
    db: Session = SessionLocal() # Obtener una sesión de base de datos
    try:
        print("Iniciando siembra de datos...")

        # --- Limpiar datos existentes (opcional, pero útil para un seed repetible) ---
        # ADVERTENCIA: Esto eliminará TODOS los datos de estas tablas.
        # Comenta o descomenta estas líneas según necesites.
        # print("Limpiando datos existentes (productos, categorías, usuarios)...")
        # db.query(models.Product).delete()
        # db.query(models.Category).delete()
        # db.query(models.User).delete()
        # db.commit() # Importante hacer commit después de los deletes
        # print("Datos existentes limpiados.")

        # --- Crear Categorías ---
        # Verificar si ya existen para no duplicar (ejemplo simple)
        existing_smartphones = db.query(models.Category).filter(models.Category.name == "Smartphones").first()
        if not existing_smartphones:
            print("Creando categoría Smartphones...")
            categoria_smartphones = models.Category(name="Smartphones", description="Teléfonos móviles inteligentes y accesorios")
            db.add(categoria_smartphones)
        else:
            print("Categoría Smartphones ya existe.")
            categoria_smartphones = existing_smartphones
        
        existing_laptops = db.query(models.Category).filter(models.Category.name == "Laptops").first()
        if not existing_laptops:
            print("Creando categoría Laptops...")
            categoria_laptops = models.Category(name="Laptops", description="Ordenadores portátiles y accesorios")
            db.add(categoria_laptops)
        else:
            print("Categoría Laptops ya existe.")
            categoria_laptops = existing_laptops

        existing_accesorios = db.query(models.Category).filter(models.Category.name == "Accesorios").first()
        if not existing_accesorios:
            print("Creando categoría Accesorios...")
            categoria_accesorios = models.Category(name="Accesorios", description="Cables, cargadores, fundas, etc.")
            db.add(categoria_accesorios)
        else:
            print("Categoría Accesorios ya existe.")
            categoria_accesorios = existing_accesorios
        
        db.commit() # Commit para que los IDs se generen y puedan ser usados por productos
        
        # Refrescar para obtener los IDs generados si se crearon nuevas
        if not existing_smartphones: db.refresh(categoria_smartphones)
        if not existing_laptops: db.refresh(categoria_laptops)
        if not existing_accesorios: db.refresh(categoria_accesorios)
        
        print(f"Categoría Smartphones (ID: {categoria_smartphones.id})")
        print(f"Categoría Laptops (ID: {categoria_laptops.id})")
        print(f"Categoría Accesorios (ID: {categoria_accesorios.id})")


        # --- Crear Usuario ---
        existing_admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not existing_admin:
            print("Creando usuario de prueba 'admin'...")
            hashed_password_admin = get_password_hash("admin123") # Cambia "admin123" por una contraseña segura
            admin_user = models.User(
                username="admin",
                email="admin@example.com",
                hashed_password=hashed_password_admin,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"Usuario creado: {admin_user.username} (ID: {admin_user.id})")
        else:
            print("Usuario 'admin' ya existe.")
            admin_user = existing_admin


        # --- Crear Productos ---
        # Producto 1
        existing_p1 = db.query(models.Product).filter(models.Product.codigo_sku == "SM-XR-BL-128").first()
        if not existing_p1:
            print("Creando producto Teléfono Estrella XR...")
            producto1 = models.Product(
                name="Teléfono Estrella XR",
                description="El último modelo con cámara increíble.",
                price=799.99,
                stock_actual=50,
                stock_minimo=10,
                codigo_sku="SM-XR-BL-128",
                category_id=categoria_smartphones.id
            )
            db.add(producto1)
            print(f"Producto añadido a la sesión: {producto1.name}")
        else:
            print("Producto Teléfono Estrella XR ya existe.")
            producto1 = existing_p1

        # Producto 2
        existing_p2 = db.query(models.Product).filter(models.Product.codigo_sku == "LP-PRO-SLV-15").first()
        if not existing_p2:
            print("Creando producto Laptop Ultrabook Pro...")
            producto2 = models.Product(
                name="Laptop Ultrabook Pro",
                description="Potente y ligera para profesionales.",
                price=1299.50,
                stock_actual=30,
                stock_minimo=5,
                codigo_sku="LP-PRO-SLV-15",
                category_id=categoria_laptops.id
            )
            db.add(producto2)
            print(f"Producto añadido a la sesión: {producto2.name}")
        else:
            print("Producto Laptop Ultrabook Pro ya existe.")
            producto2 = existing_p2

        # Producto 3
        existing_p3 = db.query(models.Product).filter(models.Product.codigo_sku == "ACC-USBC-2M").first()
        if not existing_p3:
            print("Creando producto Cable USB-C...")
            producto3 = models.Product(
                name="Cable USB-C de Carga Rápida",
                description="Cable trenzado de 2 metros, alta durabilidad.",
                price=19.99,
                stock_actual=200,
                stock_minimo=20,
                codigo_sku="ACC-USBC-2M",
                category_id=categoria_accesorios.id
            )
            db.add(producto3)
            print(f"Producto añadido a la sesión: {producto3.name}")
        else:
            print("Producto Cable USB-C ya existe.")
            producto3 = existing_p3
        
        # Producto Sin Categoría
        existing_p4 = db.query(models.Product).filter(models.Product.codigo_sku == "MB-001").first()
        if not existing_p4:
            print("Creando producto Mistery Box...")
            producto_sin_categoria = models.Product(
                name="Mistery Box",
                description="Una caja misteriosa.",
                price=9.99,
                stock_actual=10,
                stock_minimo=2,
                codigo_sku="MB-001",
                category_id=None 
            )
            db.add(producto_sin_categoria)
            print(f"Producto añadido a la sesión: {producto_sin_categoria.name}")
        else:
            print("Producto Mistery Box ya existe.")
            producto_sin_categoria = existing_p4

        db.commit() # Commit final para todos los productos añadidos
        print("Commit final de productos realizado.")

        print("\n✅ Siembra de datos completada exitosamente.")

    except Exception as e:
        db.rollback() # Revertir cambios si algo falla
        print(f"\n❌ Error durante la siembra de datos: {e}")
        import traceback
        traceback.print_exc() # Imprimir el traceback completo para más detalles del error
    finally:
        db.close() # Asegurarse de cerrar la sesión
        print("Sesión de base de datos cerrada.")

if __name__ == "__main__":
    print("Ejecutando script de siembra de datos (seed_db.py)...")
    seed_data()
    print("Script de siembra finalizado.")