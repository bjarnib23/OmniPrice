from pydantic import BaseModel
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    sku: str
    category: str | None = None


class ProductRead(ProductCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
