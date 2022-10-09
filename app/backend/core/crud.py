from sqlalchemy.orm import Session

from app.backend.core import models


def get_stock_symbol_list(db: Session):
    """get all distinct stock series values"""
    return (
        db.query(models.Stocks)
        .distinct(models.Stocks.symbol)
        .with_entities(models.Stocks.symbol)
        .all()
    )


def get_stock_by_symbol_date(db: Session, symbol: str, date: str):
    """get closing stocks model for given series & date"""
    return (
        db.query(models.Stocks)
        .filter(models.Stocks.symbol == symbol, models.Stocks.date == date)
        .with_entities(models.Stocks.closing_price)
        .one_or_none()
    )
