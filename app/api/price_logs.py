from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.price_log import PriceLog
from app.schemas.price_log import PriceLogCreate, PriceLogRead

router = APIRouter()


@router.get("/", response_model=list[PriceLogRead])
def list_price_logs(competitor_link_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(PriceLog)
    if competitor_link_id:
        query = query.filter(PriceLog.competitor_link_id == competitor_link_id)
    return query.order_by(PriceLog.scraped_at.desc()).all()


@router.post("/", response_model=PriceLogRead, status_code=201)
def create_price_log(payload: PriceLogCreate, db: Session = Depends(get_db)):
    log = PriceLog(**payload.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
