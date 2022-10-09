from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint, Date
from app.backend.core.database import Base


class Stocks(Base):
    """Stocks ORM"""
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    series = Column(String, nullable=True)
    closing_price = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    __tablename__ = "stocks"
    __table_args__ = (
        UniqueConstraint("symbol", "series", "date", name="symbol_series_date_unique_constraint"),
    )
