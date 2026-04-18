from pydantic import BaseModel
from datetime import datetime


class CompetitorLinkCreate(BaseModel):
    product_id: int
    store_id: int
    url: str


class CompetitorLinkRead(CompetitorLinkCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
