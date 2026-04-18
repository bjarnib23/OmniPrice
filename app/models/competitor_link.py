from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class CompetitorLink(Base):
    __tablename__ = "competitor_links"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    url = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    product = relationship("Product", back_populates="competitor_links")
    store = relationship("Store", back_populates="competitor_links")
    price_logs = relationship("PriceLog", back_populates="competitor_link")
