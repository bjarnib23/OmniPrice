from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    base_url = Column(String, nullable=False, unique=True)
    currency = Column(String, default="ISK")
    created_at = Column(DateTime, server_default=func.now())

    competitor_links = relationship("CompetitorLink", back_populates="store")
