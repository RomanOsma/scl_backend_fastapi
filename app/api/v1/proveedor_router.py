# app/api/v1/proveedor_router.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import proveedor_schemas
from app.crud import proveedor_crud
from app.db import models
from app.api.deps import get_current_active_user

router = APIRouter()

@router.post("/", response_model=proveedor_schemas.Proveedor, status_code=status.HTTP_201_CREATED)
def create_new_proveedor(
    proveedor_in: proveedor_schemas.ProveedorCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return proveedor_crud.create_proveedor(db=db, proveedor=proveedor_in)

@router.get("/", response_model=List[proveedor_schemas.Proveedor])
def read_all_proveedores(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
    # current_user: models.User = Depends(get_current_active_user), # Opcional proteger listado
):
    return proveedor_crud.get_proveedores(db, skip=skip, limit=limit)

@router.get("/{proveedor_id}", response_model=proveedor_schemas.Proveedor)
def read_single_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    db_proveedor = proveedor_crud.get_proveedor(db, proveedor_id=proveedor_id)
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor not found")
    return db_proveedor

@router.put("/{proveedor_id}", response_model=proveedor_schemas.Proveedor)
def update_existing_proveedor(
    proveedor_id: int,
    proveedor_in: proveedor_schemas.ProveedorUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    updated_proveedor = proveedor_crud.update_proveedor(
        db, proveedor_id=proveedor_id, proveedor_update=proveedor_in
    )
    if updated_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor not found")
    return updated_proveedor

@router.delete("/{proveedor_id}", response_model=proveedor_schemas.Proveedor)
def delete_existing_proveedor(
    proveedor_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    deleted_proveedor = proveedor_crud.delete_proveedor(db, proveedor_id=proveedor_id)
    if deleted_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor not found")
    return deleted_proveedor