from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.competitor_link import CompetitorLink
from app.schemas.competitor_link import CompetitorLinkCreate, CompetitorLinkRead

router = APIRouter()


@router.get("/", response_model=list[CompetitorLinkRead])
def list_competitor_links(product_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(CompetitorLink)
    if product_id:
        query = query.filter(CompetitorLink.product_id == product_id)
    return query.all()


@router.post("/", response_model=CompetitorLinkRead, status_code=201)
def create_competitor_link(payload: CompetitorLinkCreate, db: Session = Depends(get_db)):
    link = CompetitorLink(**payload.model_dump())
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@router.delete("/{link_id}", status_code=204)
def delete_competitor_link(link_id: int, db: Session = Depends(get_db)):
    link = db.query(CompetitorLink).filter(CompetitorLink.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="CompetitorLink not found")
    db.delete(link)
    db.commit()
