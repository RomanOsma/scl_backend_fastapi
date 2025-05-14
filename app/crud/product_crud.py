# app/crud/product_crud.py

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload # joinedload para carga eficiente de relaciones

from app.db import models
from app.schemas import product_schemas

# --- Operaciones de Lectura (Read) ---

def get_product(db: Session, product_id: int) -> Optional[models.Product]: # <--- El parámetro es product_id
    """
    Obtiene un producto específico por su ID, incluyendo su categoría.
    """
    return (
        db.query(models.Product)
        .options(joinedload(models.Product.category)) # Carga la categoría relacionada en la misma consulta
        .filter(models.Product.id == product_id)
        .first()
    )

def get_products(
    db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None
) -> List[models.Product]:
    """
    Obtiene una lista de productos, con paginación opcional y filtro por category_id.
    Incluye las categorías de los productos.
    """
    query = db.query(models.Product).options(joinedload(models.Product.category))
    
    if category_id is not None:
        query = query.filter(models.Product.category_id == category_id)
        
    return query.offset(skip).limit(limit).all()

def get_product_by_sku(db: Session, sku: str) -> Optional[models.Product]:
    """
    Obtiene un producto específico por su código SKU.
    """
    if not sku: # No buscar si SKU es None o vacío
        return None
    return db.query(models.Product).filter(models.Product.codigo_sku == sku).first()


# --- Operación de Creación (Create) ---

def create_product(db: Session, product: product_schemas.ProductCreate) -> models.Product:
    """
    Crea un nuevo producto en la base de datos.
    """
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock_actual=product.stock_actual,
        stock_minimo=product.stock_minimo,
        codigo_sku=product.codigo_sku,
        numero_serie=product.numero_serie,
        category_id=product.category_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # Para que la categoría se cargue en el objeto retornado después de crearlo:
    # Volvemos a consultarlo, ya que db.refresh no carga relaciones por defecto.
    # Esto asegura que el objeto retornado tenga la 'category' poblada si la API la espera.
    return get_product(db, product_id=db_product.id)


# --- Operación de Actualización (Update) ---

def update_product(
    db: Session, product_id: int, product_update: product_schemas.ProductUpdate
) -> Optional[models.Product]:
    """
    Actualiza un producto existente.
    """
    db_product = get_product(db, product_id=product_id) # Reutilizamos get_product para cargar con categoría
    if not db_product:
        return None

    update_data = product_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # De nuevo, volvemos a consultar para asegurar que la relación category esté actualizada
    # si el category_id fue modificado.
    return get_product(db, product_id=db_product.id)


# --- Operación de Eliminación (Delete) ---

def delete_product(db: Session, product_id: int) -> Optional[models.Product]:
    """
    Elimina un producto existente.
    """
    db_product = get_product(db, product_id=product_id) # Reutilizamos get_product
    if not db_product:
        return None

    db.delete(db_product)
    db.commit()
    return db_product # Retorna el objeto eliminado (con su categoría cargada)