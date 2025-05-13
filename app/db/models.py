# app/db/models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    ForeignKey,
    DateTime, # ¡NUEVO! Para el campo fecha
    # UniqueConstraint, # Ya lo teníamos
    # Index # Ya lo teníamos
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # Para server_default=func.now()

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # ¡NUEVA RELACIÓN! Un usuario puede ser responsable de muchos movimientos de inventario
    movimientos_inventario = relationship("MovimientoInventario", back_populates="responsable")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"

# ¡NUEVO MODELO!
class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False, index=True)
    # 'contacto' podría dividirse en más campos si fuera necesario (nombre_contacto, email_contacto, telefono_contacto)
    # Por simplicidad, lo dejamos como un solo campo de texto por ahora.
    # O podríamos hacerlo más estructurado:
    contacto_nombre = Column(String(100), nullable=True)
    contacto_email = Column(String(100), nullable=True) # Podría tener validación de email
    contacto_telefono = Column(String(30), nullable=True)
    direccion = Column(Text, nullable=True)

    # Relación: Un proveedor puede tener muchos productos
    products = relationship("Product", back_populates="proveedor")

    def __repr__(self):
        return f"<Proveedor(id={self.id}, nombre='{self.nombre}')>"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock_actual = Column(Integer, default=0, nullable=False)
    stock_minimo = Column(Integer, default=0, nullable=False)
    codigo_sku = Column(String(100), unique=True, index=True, nullable=True)
    numero_serie = Column(String(100), unique=True, nullable=True) # Asumiendo único por instancia de producto

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="products")

    # ¡NUEVO CAMPO Y RELACIÓN!
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=True) # Un producto puede no tener proveedor
    proveedor = relationship("Proveedor", back_populates="products")

    # ¡NUEVA RELACIÓN! Un producto puede tener muchos movimientos de inventario
    movimientos_inventario = relationship("MovimientoInventario", back_populates="producto", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}')>"


# ¡NUEVO MODELO!
class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"

    id = Column(Integer, primary_key=True, index=True)
    
    producto_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    # Tipo de movimiento: 'ENTRADA', 'SALIDA', 'AJUSTE_INICIAL', 'AJUSTE_CONTEO_MAS', 'AJUSTE_CONTEO_MENOS', 'DEVOLUCION', etc.
    # Podríamos usar un Enum de Python aquí si quisiéramos ser más estrictos,
    # pero un String es flexible para empezar.
    tipo_movimiento = Column(String(50), nullable=False)
    cantidad = Column(Integer, nullable=False) # Positivo para entradas/ajustes+, negativo para salidas/ajustes-
                                               # O siempre positivo y el 'tipo_movimiento' define la dirección.
                                               # Mantenerlo siempre positivo y que 'tipo_movimiento' defina
                                               # la operación (+ o -) sobre el stock es más claro.
    
    fecha = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    responsable_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Quién registró el movimiento (puede ser NULL si es automático)
    notas = Column(Text, nullable=True)

    producto = relationship("Product", back_populates="movimientos_inventario")
    responsable = relationship("User", back_populates="movimientos_inventario")

    def __repr__(self):
        return f"<MovimientoInventario(id={self.id}, producto_id={self.producto_id}, tipo='{self.tipo_movimiento}', cantidad={self.cantidad})>"