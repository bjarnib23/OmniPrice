import json
import re
from typing import Optional


def extract_from_jsonld(html: str) -> Optional[dict]:
    pattern = r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    matches = re.findall(pattern, html, re.DOTALL)

    for raw in matches:
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                data = data[0]
            if data.get("@type") in ("Product", "Offer"):
                return _normalize(data)
        except (json.JSONDecodeError, AttributeError):
            continue
    return None


def _normalize(data: dict) -> dict:
    offers = data.get("offers", {})
    if isinstance(offers, list):
        offers = offers[0]

    price = offers.get("price") or data.get("price")
    in_stock = "InStock" in (offers.get("availability", "") or "")

    return {
        "name": data.get("name"),
        "price": float(price) if price else None,
        "in_stock": in_stock,
        "source": "jsonld",
    }
