from pydantic import BaseModel
from datetime import datetime


class PriceLogCreate(BaseModel):
    competitor_link_id: int
    price: float
    currency: str = "ISK"
    in_stock: bool = True


class PriceLogRead(PriceLogCreate):
    id: int
    scraped_at: datetime

    model_config = {"from_attributes": True}
