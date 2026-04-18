from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead

router = APIRouter()


@router.get("/", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductRead, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
