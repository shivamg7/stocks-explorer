from sqlalchemy.orm import Session

from app.backend.core import models


def get_stock_series_list(db: Session):
    """get all distinct stock series values"""
    return (
        db.query(models.Stocks)
        .distinct(models.Stocks.series)
        .with_entities(models.Stocks.series)
        .all()
    )


def get_stock_by_series_date(db: Session, series: str, date: str):
    """get closing stocks model for given series & date"""
    return (
        db.query(models.Stocks)
        .filter(models.Stocks.series == series, models.Stocks.date == date)
        .with_entities(models.Stocks.closing_price)
        .one_or_none()
    )
