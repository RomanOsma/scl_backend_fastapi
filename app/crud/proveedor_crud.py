# app/crud/proveedor_crud.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db import models
from app.schemas import proveedor_schemas

def get_proveedor(db: Session, proveedor_id: int) -> Optional[models.Proveedor]:
    return db.query(models.Proveedor).filter(models.Proveedor.id == proveedor_id).first()

def get_proveedores(db: Session, skip: int = 0, limit: int = 100) -> List[models.Proveedor]:
    return db.query(models.Proveedor).offset(skip).limit(limit).all()

def create_proveedor(db: Session, proveedor: proveedor_schemas.ProveedorCreate) -> models.Proveedor:
    db_proveedor = models.Proveedor(**proveedor.model_dump())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

def update_proveedor(db: Session, proveedor_id: int, proveedor_update: proveedor_schemas.ProveedorUpdate) -> Optional[models.Proveedor]:
    db_proveedor = get_proveedor(db, proveedor_id)
    if not db_proveedor:
        return None
    update_data = proveedor_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_proveedor, key, value)
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

def delete_proveedor(db: Session, proveedor_id: int) -> Optional[models.Proveedor]:
    db_proveedor = get_proveedor(db, proveedor_id)
    if not db_proveedor:
        return None
    db.delete(db_proveedor)
    db.commit()
    return db_proveedor