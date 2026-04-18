from pydantic import BaseModel
from datetime import datetime


class StoreCreate(BaseModel):
    name: str
    base_url: str
    currency: str = "ISK"


class StoreRead(StoreCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
