# app/schemas/__init__.py
from .category_schemas import Category, CategoryCreate, CategoryUpdate, CategoryBase
from .product_schemas import Product, ProductCreate, ProductUpdate, ProductBase
from .user_schemas import User, UserCreate, UserUpdate, UserBase
from .token_schemas import Token, TokenData
from .proveedor_schemas import Proveedor, ProveedorCreate, ProveedorUpdate, ProveedorBase # ¡NUEVO!
from .movimiento_inventario_schemas import MovimientoInventario, MovimientoInventarioCreate, MovimientoInventarioBase, UserSimple, ProductSimple # ¡NUEVO!