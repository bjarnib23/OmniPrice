from Levenshtein import ratio
from sqlalchemy.orm import Session
from app.models.price_log import PriceLog
from app.models.competitor_link import CompetitorLink


SIMILARITY_THRESHOLD = 0.75


def are_same_product(name_a: str, name_b: str) -> bool:
    return ratio(name_a.lower(), name_b.lower()) >= SIMILARITY_THRESHOLD


def get_latest_prices(product_id: int, db: Session) -> list[dict]:
    links = (
        db.query(CompetitorLink)
        .filter(CompetitorLink.product_id == product_id)
        .all()
    )

    results = []
    for link in links:
        latest = (
            db.query(PriceLog)
            .filter(PriceLog.competitor_link_id == link.id)
            .order_by(PriceLog.scraped_at.desc())
            .first()
        )
        if latest:
            results.append({
                "store_id": link.store_id,
                "url": link.url,
                "price": latest.price,
                "in_stock": latest.in_stock,
                "scraped_at": latest.scraped_at,
            })

    return sorted(results, key=lambda x: x["price"])


def detect_anomaly(prices: list[float], new_price: float) -> bool:
    if len(prices) < 3:
        return False
    avg = sum(prices) / len(prices)
    return new_price < avg * 0.7  # flag if more than 30% below average
