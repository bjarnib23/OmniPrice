from sqlalchemy.orm import Session
from app.crawler.scraper import fetch_page
from app.parser.jsonld_parser import extract_from_jsonld
from app.parser.llm_parser import extract_with_llm
from app.models.competitor_link import CompetitorLink
from app.models.price_log import PriceLog


async def scrape_competitor_link(link_id: int, db: Session) -> dict:
    link = db.query(CompetitorLink).filter(CompetitorLink.id == link_id).first()
    if not link:
        raise ValueError(f"CompetitorLink {link_id} not found")

    html = await fetch_page(link.url)

    result = extract_from_jsonld(html)
    if not result or result["price"] is None:
        result = await extract_with_llm(html)

    if not result or result["price"] is None:
        raise ValueError(f"Could not extract price from {link.url}")

    log = PriceLog(
        competitor_link_id=link.id,
        price=result["price"],
        in_stock=result.get("in_stock", True),
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return {
        "competitor_link_id": link.id,
        "url": link.url,
        "price": log.price,
        "in_stock": log.in_stock,
        "source": result.get("source"),
        "scraped_at": log.scraped_at,
    }
