from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, index=True)
    category = Column(String)
    created_at = Column(DateTime, server_default=func.now())

    competitor_links = relationship("CompetitorLink", back_populates="product")
