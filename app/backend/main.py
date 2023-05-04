from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from app.backend.core import crud
from app.backend.core.database import SessionLocal

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/frontend", StaticFiles(directory="app/frontend/stock-explorer/dist/stock-explorer/", html=True), name="ui")


def get_db():
    """Get a session object for db transactions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return RedirectResponse(url="/frontend/index.html")


@app.get("/stocks")
def all_stocks(db: Session = Depends(get_db)):
    stocks = crud.get_stock_symbol_list(db=db)
    return stocks


@app.get("/stocks/series")
def get_stock_by_series_date(symbol: str, start_date: str, end_date: str, db: Session = Depends(get_db)):
    stock = crud.get_stock_by_symbol_date(db=db, symbol=symbol, start_date=start_date, end_date=end_date)
    if not stock:
        raise HTTPException(status_code=404, detail="data not found")
    return stock
