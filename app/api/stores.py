from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.store import Store
from app.schemas.store import StoreCreate, StoreRead

router = APIRouter()


@router.get("/", response_model=list[StoreRead])
def list_stores(db: Session = Depends(get_db)):
    return db.query(Store).all()


@router.get("/{store_id}", response_model=StoreRead)
def get_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.post("/", response_model=StoreRead, status_code=201)
def create_store(payload: StoreCreate, db: Session = Depends(get_db)):
    store = Store(**payload.model_dump())
    db.add(store)
    db.commit()
    db.refresh(store)
    return store


@router.delete("/{store_id}", status_code=204)
def delete_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    db.delete(store)
    db.commit()
