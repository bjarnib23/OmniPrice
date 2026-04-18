from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crawler.scrape_job import scrape_competitor_link

router = APIRouter()


@router.post("/{link_id}")
async def scrape(link_id: int, db: Session = Depends(get_db)):
    try:
        result = await scrape_competitor_link(link_id, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scrape failed: {str(e)}")
