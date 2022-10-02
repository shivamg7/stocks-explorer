from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint, Date
from app.backend.core.database import Base


class Stocks(Base):
    """Stocks ORM"""
    id = Column(Integer, primary_key=True)
    series = Column(String, nullable=False)
    closing_price = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    __tablename__ = "stocks"
    __table_args__ = (
        UniqueConstraint("series", "date", name="series_date_unique_constraint"),
    )
