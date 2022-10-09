from sqlalchemy.orm import Session
from sqlalchemy.dialects import postgresql

from app.backend.core import models


def get_stock_symbol_list(db: Session):
    """get all distinct stock series values"""
    return (
        db.query(models.Stocks)
        .distinct(models.Stocks.symbol)
        .with_entities(models.Stocks.symbol)
        .all()
    )


def get_stock_by_symbol_date(db: Session, symbol: str, start_date: str, end_date: str):
    """get closing stocks model for given series & date"""
    print(db.query(models.Stocks)
        .filter(models.Stocks.symbol == symbol, models.Stocks.date >= start_date, models.Stocks.date <= end_date)
        .with_entities(models.Stocks.closing_price, models.Stocks.date).statement.compile(dialect=postgresql.dialect()))
    print(symbol, start_date, end_date)
    return (
        db.query(models.Stocks)
        .filter(models.Stocks.symbol == symbol, models.Stocks.date >= start_date, models.Stocks.date <= end_date)
        .with_entities(models.Stocks.closing_price, models.Stocks.date)
        .all()
    )
