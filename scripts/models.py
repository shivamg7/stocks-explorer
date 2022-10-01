from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

Base = declarative_base()


class Stocks(Base):
    """"""
    id = Column(Integer, primary_key=True)
    series = Column(String, not_null=True)
    closing_price = Column(Float, not_null=True)
    date = Column(DateTime, not_null=True)

    __tablename__ = "stocks"
