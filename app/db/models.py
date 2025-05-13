# app/db/models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float, # Para precios, considera Numeric para mayor precisión con dinero
    Boolean,
    Text,
    ForeignKey,
    UniqueConstraint, # Para restricciones únicas
    Index # Para índices
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text # Para valores por defecto a nivel de BD, ej: server_default

from .database import Base # Importa la Base declarativa desde tu archivo database.py

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False) # Longitud y nombre de constraint
    email = Column(String(100), unique=True, index=True, nullable=True) # Longitud y nombre de constraint
    hashed_password = Column(String, nullable=False) # Longitud podría ser String(60) o más para bcrypt
    is_active = Column(Boolean, default=True, nullable=False) 
    server_default=text('true') # también es una opción

    # --- Relaciones (se añadirán más adelante cuando definamos otros modelos) ---
    # productos_responsable = relationship("Product", back_populates="responsable_creacion")
    # movimientos_inventario = relationship("MovimientoInventario", back_populates="responsable")

    # --- Restricciones a nivel de tabla (alternativa a unique=True en Column) ---
    # __table_args__ = (
    #     UniqueConstraint('username', name='uq_user_username'),
    #     UniqueConstraint('email', name='uq_user_email'),
    # )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relación: Una categoría puede tener muchos productos
    products = relationship("Product", back_populates="category")

    # __table_args__ = (
    #     UniqueConstraint('name', name='uq_category_name'),
    # )

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True) # Índice en name para búsquedas
    description = Column(Text, nullable=True)
    # Para dinero, es mejor usar Numeric, pero Float es más simple para empezar
    # from sqlalchemy import Numeric
    # price = Column(Numeric(10, 2), nullable=False)
    price = Column(Float, nullable=False)
    stock_actual = Column(Integer, default=0, nullable=False)
    stock_minimo = Column(Integer, default=0, nullable=False)
    codigo_sku = Column(String(100), unique=True, index=True, nullable=True) # SKU debe ser único si existe
    numero_serie = Column(String(100), unique=True, nullable=True) # Número de serie único si aplica por producto
                                                                  # Si un producto puede tener múltiples números de serie
                                                                  # individuales, esta lógica debería ser diferente.

    # Clave Foránea para la categoría
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True) # Un producto podría no tener categoría

    # Relación: Un producto pertenece a una categoría
    category = relationship("Category", back_populates="products")

    # --- Otras relaciones y campos (se añadirán más adelante) ---
    # proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=True)
    # proveedor = relationship("Proveedor", back_populates="products")
    #
    # responsable_creacion_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # responsable_creacion = relationship("User", back_populates="productos_responsable")
    #
    # fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    # fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())


    # --- Restricciones e Índices ---
    # __table_args__ = (
    #     UniqueConstraint('codigo_sku', name='uq_product_codigo_sku'),
    #     UniqueConstraint('numero_serie', name='uq_product_numero_serie'), # Si debe ser único
    #     Index('ix_product_name', 'name'), # Índice explícito en nombre
    # )

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}')>"

# --- Modelos para Proveedores y Movimientos de Inventario (se añadirán en FASES POSTERIORES) ---
# class Proveedor(Base):
#     __tablename__ = "proveedores"
#     id = Column(Integer, primary_key=True, index=True)
#     nombre = Column(String(150), nullable=False, index=True)
#     contacto_nombre = Column(String(100), nullable=True)
#     contacto_email = Column(String(100), nullable=True)
#     contacto_telefono = Column(String(20), nullable=True)
#     direccion = Column(Text, nullable=True)
#     products = relationship("Product", back_populates="proveedor")

# class MovimientoInventario(Base):
#     __tablename__ = "movimientos_inventario"
#     id = Column(Integer, primary_key=True, index=True)
#     producto_id = Column(Integer, ForeignKey("products.id"), nullable=False)
#     tipo_movimiento = Column(String(50), nullable=False) # ej: 'ENTRADA', 'SALIDA', 'AJUSTE_POSITIVO', 'AJUSTE_NEGATIVO'
#     cantidad = Column(Integer, nullable=False)
#     fecha = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
#     responsable_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Quién hizo el movimiento
#     notas = Column(Text, nullable=True)
#
#     product = relationship("Product") # No necesita back_populates si Product no necesita la lista directa
#     responsable = relationship("User", back_populates="movimientos_inventario")