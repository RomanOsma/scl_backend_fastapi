# scl_backend_fastapi/seed_db.py

import sys
import os
from datetime import datetime, timedelta, timezone
import random
from faker import Faker # Para generar datos falsos más realistas

# --- Configuración de sys.path ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError # Para manejar errores de constraints
from app.db.database import SessionLocal, engine, Base
from app.db import models
from app.security.auth_security import get_password_hash

# --- Crear todas las tablas ---
print("Intentando crear tablas si no existen (Alembic ya debería haberlas creado)...")
try:
    Base.metadata.create_all(bind=engine)
    print("Verificación/creación de tablas completada.")
except Exception as e:
    print(f"Error durante Base.metadata.create_all: {e}")
    sys.exit(1)

fake = Faker(['es_ES', 'en_US']) # Instancia de Faker, puedes añadir más localizaciones

def get_or_create(db_session: Session, model, defaults: dict = None, **kwargs):
    """
    Obtiene una instancia si existe (basado en kwargs), de lo contrario la crea.
    Retorna la instancia y un booleano 'created'.
    """
    instance = db_session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = {**kwargs, **(defaults or {})}
        instance = model(**params)
        try:
            db_session.add(instance)
            db_session.commit() # Commit individual para obtener el ID si es nuevo
            db_session.refresh(instance)
            return instance, True
        except IntegrityError: # Captura error si, por ej, una restricción unique falla por una condición de carrera
            db_session.rollback()
            # Intenta obtenerlo de nuevo, quizás otro proceso lo creó justo ahora
            instance = db_session.query(model).filter_by(**kwargs).first()
            if instance:
                return instance, False
            else: # Si sigue sin existir después del rollback, algo más está mal
                print(f"CRITICAL ERROR: Could not get or create {model.__name__} with {kwargs} after IntegrityError.")
                raise 
        except Exception as e_create:
            db_session.rollback()
            print(f"Error crítico creando instancia de {model.__name__} con {params}: {e_create}")
            raise

def seed_data():
    db: Session = SessionLocal()
    try:
        print("Iniciando siembra de datos IDEMPOTENTE Y EXTENSA...")

        # --- Limpiar datos existentes (OPCIONAL) ---
        # Descomenta estas líneas si quieres un borrado completo antes de sembrar.
        # El orden es importante debido a las claves foráneas.
        print("Limpiando datos existentes (movimientos, productos, proveedores, categorías, usuarios)...")
        db.query(models.MovimientoInventario).delete(synchronize_session=False)
        db.query(models.Product).delete(synchronize_session=False)
        db.query(models.Proveedor).delete(synchronize_session=False)
        db.query(models.Category).delete(synchronize_session=False)
        db.query(models.User).delete(synchronize_session=False)
        db.commit()
        print("Datos existentes limpiados.")

        # --- Crear Usuarios (si no existen) ---
        print("\n--- Procesando Usuarios ---")
        users_data = [
            {"username": "admin_stock", "defaults": {"email": "admin.stock@example.com", "hashed_password": get_password_hash("StrongPass123!"), "is_active": True}},
            {"username": "ana_ventas", "defaults": {"email": "ana.ventas@example.com", "hashed_password": get_password_hash("AnaPass456_"), "is_active": True}},
            {"username": "juan_almacen", "defaults": {"email": "juan.almacen@example.com", "hashed_password": get_password_hash("JuanStore789="), "is_active": True}},
            {"username": "laura_compras", "defaults": {"email": "laura.compras@example.com", "hashed_password": get_password_hash("LauraBuy00!"), "is_active": True}},
            {"username": "pedro_soporte", "defaults": {"email": "pedro.soporte@example.com", "hashed_password": get_password_hash("PedroHelp_11"), "is_active": False}}, # Un usuario inactivo
        ]
        created_users_map = {} # Para acceder a los objetos User por username
        for u_data in users_data:
            user, created = get_or_create(db, models.User, username=u_data["username"], defaults=u_data["defaults"])
            created_users_map[user.username] = user
            if created:
                print(f"  Usuario CREADO: {user.username} (ID: {user.id})")
            else:
                print(f"  Usuario YA EXISTÍA: {user.username} (ID: {user.id})")
        
        # --- Crear Categorías (si no existen) ---
        print("\n--- Procesando Categorías ---")
        categories_data = [
            {"name": "Smartphones", "defaults": {"description": "Teléfonos inteligentes de última generación"}},
            {"name": "Laptops", "defaults": {"description": "Portátiles para trabajo y ocio"}},
            {"name": "Tablets", "defaults": {"description": "Dispositivos táctiles portátiles"}},
            {"name": "Accesorios", "defaults": {"description": "Cargadores, fundas, cables, teclados, ratones"}},
            {"name": "Componentes PC", "defaults": {"description": "Hardware interno: CPUs, GPUs, RAM, Placas Base"}},
            {"name": "Audio y Video", "defaults": {"description": "Auriculares, altavoces, monitores, proyectores"}},
        ]
        created_categories_map = {}
        for c_data in categories_data:
            cat, created = get_or_create(db, models.Category, name=c_data["name"], defaults=c_data["defaults"])
            created_categories_map[cat.name] = cat
            if created:
                print(f"  Categoría CREADA: {cat.name} (ID: {cat.id})")
            else:
                print(f"  Categoría YA EXISTÍA: {cat.name} (ID: {cat.id})")

        # --- Crear Proveedores (si no existen) ---
        print("\n--- Procesando Proveedores ---")
        proveedores_data = [
            {"nombre": "ElectroTech Global", "defaults": {"contacto_nombre": "Carlos Fuentes", "contacto_email": fake.company_email(), "contacto_telefono": fake.phone_number(), "direccion": fake.address()}},
            {"nombre": "GadgetSupply Co.", "defaults": {"contacto_nombre": "Laura Méndez", "contacto_email": fake.company_email(), "contacto_telefono": fake.phone_number(), "direccion": fake.address()}},
            {"nombre": "Componentes Avanzados S.A.", "defaults": {"contacto_nombre": "Pedro Ramírez", "contacto_email": fake.company_email(), "contacto_telefono": fake.phone_number(), "direccion": fake.address()}},
            {"nombre": "Soluciones Digitales Rápidas", "defaults": {"contacto_nombre": "Sofía Castillo", "contacto_email": fake.company_email(), "contacto_telefono": fake.phone_number(), "direccion": fake.address()}},
        ]
        created_proveedores_map = {}
        for p_data in proveedores_data:
            prov, created = get_or_create(db, models.Proveedor, nombre=p_data["nombre"], defaults=p_data["defaults"])
            created_proveedores_map[prov.nombre] = prov
            if created:
                print(f"  Proveedor CREADO: {prov.nombre} (ID: {prov.id})")
            else:
                print(f"  Proveedor YA EXISTÍA: {prov.nombre} (ID: {prov.id})")

        # --- Crear Productos y Movimientos Iniciales ---
        print("\n--- Procesando Productos y Movimientos Iniciales ---")
        productos_defs = [
            {"sku": "APH-X1", "n": "AlphaPhone X1", "d": "Smartphone premium con IA", "p": 999.99, "s_min": 5, "cat_n": "Smartphones", "prov_n": "ElectroTech Global", "stock_ini": 25, "ns_base": "APHX1"},
            {"sku": "ZBP-16", "n": "ZetaBook Pro 16", "d": "Laptop para creativos", "p": 2199.00, "s_min": 3, "cat_n": "Laptops", "prov_n": "GadgetSupply Co.", "stock_ini": 15, "ns_base": "ZBP16"},
            {"sku": "OTS-S7", "n": "OmegaTab S7", "d": "Tablet versátil", "p": 449.50, "s_min": 8, "cat_n": "Tablets", "prov_n": "ElectroTech Global", "stock_ini": 30, "ns_base": "OTSS7"},
            {"sku": "CPC-USBC", "n": "Cable ProCharge USB-C", "d": "Cable de carga rápida 2m", "p": 24.99, "s_min": 20, "cat_n": "Accesorios", "prov_n": "GadgetSupply Co.", "stock_ini": 150, "ns_base": None},
            {"sku": "SSD-NV1T", "n": "SSD NvMe UltraSpeed 1TB", "d": "Almacenamiento SSD M.2", "p": 129.99, "s_min": 10, "cat_n": "Componentes PC", "prov_n": "Componentes Avanzados S.A.", "stock_ini": 40, "ns_base": "SSDNV"},
            {"sku": "PBM-20K", "n": "PowerBank Max 20000mAh", "d": "Batería externa PD", "p": 49.90, "s_min": 15, "cat_n": "Accesorios", "prov_n": "ElectroTech Global", "stock_ini": 75, "ns_base": None},
            {"sku": "SPH-SE", "n": "SigmaPhone SE", "d": "Smartphone económico", "p": 299.00, "s_min": 10, "cat_n": "Smartphones", "prov_n": "GadgetSupply Co.", "stock_ini": 50, "ns_base": "SPHSE"},
            {"sku": "MON-ULTRA27", "n": "Monitor UltraSharp 27\" QHD", "d": "Monitor QHD IPS", "p": 349.00, "s_min": 4, "cat_n": "Audio y Video", "prov_n": "ElectroTech Global", "stock_ini": 12, "ns_base": None},
            {"sku": "MOUSE-ERGOPRO", "n": "Ratón Ergonómico Pro", "d": "Ratón inalámbrico", "p": 59.95, "s_min": 8, "cat_n": "Accesorios", "prov_n": "Componentes Avanzados S.A.", "stock_ini": 60, "ns_base": None},
            {"sku": "KEY-MECHLGT", "n": "Teclado Mecánico Iluminado", "d": "Teclado compacto RGB", "p": 119.00, "s_min": 6, "cat_n": "Accesorios", "prov_n": "GadgetSupply Co.", "stock_ini": 22, "ns_base": None},
        ]
        
        created_products_map = {} # Guardar productos por SKU
        for i, p_def in enumerate(productos_defs):
            numero_serie_gen = f"{p_def['ns_base']}-{random.randint(10000, 99999)}-{i}" if p_def["ns_base"] else None
            defaults = {
                "name": p_def["n"], "description": p_def["d"], "price": p_def["p"],
                "stock_minimo": p_def["s_min"], "numero_serie": numero_serie_gen,
                "category_id": created_categories_map[p_def["cat_n"]].id,
                "proveedor_id": created_proveedores_map[p_def["prov_n"]].id,
                "stock_actual": 0 
            }
            producto, created = get_or_create(db, models.Product, codigo_sku=p_def["sku"], defaults=defaults)
            created_products_map[producto.codigo_sku] = producto 

            if created:
                print(f"  Producto CREADO: {producto.name} (SKU: {producto.codigo_sku})")
                fecha_mov_inicial = datetime.now(timezone.utc) - timedelta(days=random.randint(120, 150)) # Antigüedad para el stock inicial
                mov_inicial = models.MovimientoInventario(
                    producto_id=producto.id,
                    tipo_movimiento="AJUSTE_INICIAL",
                    cantidad=p_def["stock_ini"],
                    responsable_id=created_users_map["admin_stock"].id,
                    notas="Stock inicial al registrar producto",
                    fecha=fecha_mov_inicial
                )
                db.add(mov_inicial)
                producto.stock_actual = p_def["stock_ini"]
                db.add(producto) 
                db.commit() 
                db.refresh(producto)
                db.refresh(mov_inicial)
                print(f"    Movimiento inicial para {producto.name}: +{p_def['stock_ini']}, Stock actual: {producto.stock_actual}")
            else:
                print(f"  Producto YA EXISTÍA: {producto.name} (SKU: {producto.codigo_sku}). No se crea movimiento inicial.")
        
        # --- Simular más Movimientos de Inventario para generar historial ---
        print("\n--- Simulando Movimientos de Inventario Adicionales ---")
        TIPO_ENTRADA_PROV = "ENTRADA_PROVEEDOR"
        TIPO_SALIDA_VENTA = "SALIDA_VENTA"
        TIPO_AJUSTE_MAS = "AJUSTE_CONTEO_MAS"
        TIPO_AJUSTE_MENOS = "AJUSTE_CONTEO_MENOS"
        TIPO_DEVOLUCION = "DEVOLUCION_CLIENTE"

        responsables_activos = [user for user in created_users_map.values() if user.is_active]
        if not responsables_activos: # Asegurar que hay al menos un responsable activo
            responsables_activos = [created_users_map["admin_stock"]]


        for sku, producto_obj in created_products_map.items():
            db.refresh(producto_obj) # Asegurar que tenemos el stock_actual más reciente
            current_stock = producto_obj.stock_actual
            print(f"  Procesando movimientos adicionales para: {producto_obj.name} (Stock actual: {current_stock})")

            fecha_base_movs = datetime.now(timezone.utc) - timedelta(days=119) 

            for _ in range(random.randint(3, 7)): # 3 a 7 movimientos adicionales
                dias_offset = random.randint(0, 118) 
                fecha_mov = fecha_base_movs + timedelta(days=dias_offset)
                
                if producto_obj.movimientos_inventario: # Evitar fechas antes del movimiento inicial
                    fecha_primer_mov = min(m.fecha for m in producto_obj.movimientos_inventario if m.fecha is not None) # Añadido if m.fecha is not None
                    if fecha_primer_mov and fecha_mov < fecha_primer_mov: # Añadido if fecha_primer_mov
                        fecha_mov = fecha_primer_mov + timedelta(days=random.randint(1, 5))

                tipo_elegido = random.choices(
                    [TIPO_ENTRADA_PROV, TIPO_SALIDA_VENTA, TIPO_SALIDA_VENTA, TIPO_SALIDA_VENTA, TIPO_AJUSTE_MAS, TIPO_AJUSTE_MENOS, TIPO_DEVOLUCION],
                    weights=[0.3, 0.15, 0.15, 0.15, 0.05, 0.05, 0.15],
                    k=1
                )[0]
                
                cantidad_mov = 0
                responsable_mov = random.choice(responsables_activos)
                notas_mov = fake.sentence(nb_words=random.randint(4,8))

                if tipo_elegido == TIPO_ENTRADA_PROV:
                    cantidad_mov = random.randint(max(5, producto_obj.stock_minimo), producto_obj.stock_minimo * 3 if producto_obj.stock_minimo > 0 else 20)
                    current_stock += cantidad_mov
                    notas_mov = f"Pedido a {producto_obj.proveedor.nombre if producto_obj.proveedor else 'Proveedor Genérico'} #{fake.bothify(text='PO-####??')} - {notas_mov}"
                elif tipo_elegido == TIPO_SALIDA_VENTA:
                    if current_stock > 0:
                        cantidad_mov = random.randint(1, max(1, int(current_stock * 0.2) if current_stock > 2 else 1))
                        current_stock -= cantidad_mov
                        notas_mov = f"Factura #{fake.bothify(text='INV-??????')} - {notas_mov}"
                    else:
                        continue 
                elif tipo_elegido == TIPO_AJUSTE_MAS:
                    cantidad_mov = random.randint(1, 5)
                    current_stock += cantidad_mov
                    notas_mov = f"Ajuste positivo por conteo físico - {notas_mov}"
                elif tipo_elegido == TIPO_AJUSTE_MENOS:
                    if current_stock > 0:
                        cantidad_mov = random.randint(1, min(3, current_stock))
                        current_stock -= cantidad_mov
                        notas_mov = f"Ajuste negativo por merma o daño - {notas_mov}"
                    else:
                        continue
                elif tipo_elegido == TIPO_DEVOLUCION:
                    cantidad_mov = random.randint(1, 2)
                    current_stock += cantidad_mov
                    notas_mov = f"Devolución cliente, RMA #{fake.bothify(text='RMA-###')} - {notas_mov}"
                
                if cantidad_mov > 0:
                    mov = models.MovimientoInventario(
                        producto_id=producto_obj.id, tipo_movimiento=tipo_elegido, cantidad=cantidad_mov,
                        fecha=fecha_mov, responsable_id=responsable_mov.id, notas=notas_mov
                    )
                    db.add(mov)
                    producto_obj.stock_actual = current_stock 
                    db.add(producto_obj) 
                    print(f"    {producto_obj.name}: {tipo_elegido} {'+' if tipo_elegido in [TIPO_ENTRADA_PROV, TIPO_AJUSTE_MAS, TIPO_DEVOLUCION] else '-'}{cantidad_mov} (Fecha: {fecha_mov.strftime('%Y-%m-%d')}), Stock: {producto_obj.stock_actual}")
            
            db.commit() # Commit por cada producto para liberar memoria y persistir cambios
            print(f"  Movimientos adicionales para {producto_obj.name} y stock finalizados. Stock final: {producto_obj.stock_actual}")

        print("\n✅ Siembra de datos IDEMPOTENTE y con HISTORIAL EXTENSO finalizada exitosamente.")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error durante la siembra de datos: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        print("Sesión de base de datos cerrada.")

if __name__ == "__main__":
    print("Ejecutando script de siembra de datos avanzado, extenso e idempotente...")
    seed_data()
    print("Script de siembra avanzado, extenso e idempotente finalizado.")