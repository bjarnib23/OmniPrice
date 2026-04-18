from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class PriceLog(Base):
    __tablename__ = "price_logs"

    id = Column(Integer, primary_key=True, index=True)
    competitor_link_id = Column(Integer, ForeignKey("competitor_links.id"), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, default="ISK")
    in_stock = Column(Boolean, default=True)
    scraped_at = Column(DateTime, server_default=func.now())

    competitor_link = relationship("CompetitorLink", back_populates="price_logs")
