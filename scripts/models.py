from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint

Base = declarative_base()


class Stocks(Base):
    """"""
    id = Column(Integer, primary_key=True)
    series = Column(String, nullable=False)
    closing_price = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)

    __tablename__ = "stocks"
    __table_args__ = (
        UniqueConstraint("series", "date", name="series_date_unique_constraint"),
    )
