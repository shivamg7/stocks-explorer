from typing import Union

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.backend.core import crud
from app.backend.core.database import SessionLocal

app = FastAPI()


def get_db():
    """Get a session object for db transactions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/stocks")
def all_stocks(db: Session = Depends(get_db)):
    stocks = crud.get_stock_series_list(db=db)
    return stocks


@app.get("/stocks/{series}/{date}")
def get_stock_by_series_date(series: str, date: str, db: Session = Depends(get_db)):
    stock = crud.get_stock_by_series_date(db=db, series=series, date=date)
    if not stock:
        raise HTTPException(status_code=404, detail="stock data not found")
    return stock
