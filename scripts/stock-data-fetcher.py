# Fetch stocks from a NSE index
# Input:
#  start_date: Date time (DD-MM-YYYY)
#  end_date(Optional): Date time (DD-MM-YYYY)
#
#
# Sample Command
# python stock-data-fetcher.py --start_date 20-09-2022
# python stock-data-fetched.py --start_date 20-08-2022 20-09-2022


import argparse
import datetime
import io
import logging
import os
import tempfile
import zipfile
from http import HTTPStatus
from pathlib import Path

import pandas as pd

import requests as requests
from sqlalchemy import create_engine

from scripts.constants import STOCK_URI, StockColumns, REQUIRED_STOCK_COLUMNS
from scripts.models import Stocks

logger = logging.getLogger(__name__)
logFileHandler = logging.FileHandler(
    f"stock-data-fetcher-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}.log"
)
logger.setLevel(logging.DEBUG)
logger.addHandler(logFileHandler)


class StockFetcher:

    def __init__(self):
        """init"""
        pghost = os.getenv("PGHOST")
        pguser = os.getenv("PGUSER")
        pgport = os.getenv("PGPORT")
        pgpassword = os.getenv("PGPASSWORD")
        database_name = os.getenv("DATABASE_NAME")

        self.engine = create_engine(f"postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{database_name}")
        self.end_date = None
        self.start_date = None

    @staticmethod
    def parse_date_format(date: str) -> datetime.date:
        """Validate & parse date input"""
        try:
            parsed_date = datetime.datetime.strptime(date, "%d-%m-%Y").date()
            return parsed_date
        except ValueError as e:
            logger.error(e)
            raise Exception(f"Invalid date input {date}")

    @staticmethod
    def fetch_stocks(date: datetime.date) -> pd.DataFrame:
        """Fetch stocks from NSE index"""
        request_uri = STOCK_URI.format(
            date.strftime("%Y"),
            date.strftime("%b").upper(),
            date.strftime("%d"),
            date.strftime("%b").upper(),
            date.strftime("%Y")
        )

        logger.info(f"making request for date {date}")
        response = requests.get(request_uri)

        if response.status_code != HTTPStatus.OK:
            logger.error(f"error while fetching content from uri {request_uri}, return code: {response.status_code}")
            return pd.DataFrame(columns=REQUIRED_STOCK_COLUMNS)

        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        zip_file_members = zip_file.namelist()

        if len(zip_file_members) != 1:
            logger.error(f"unexpected files returned from stock api, number of members in archive {zip_file_members}")

        member_to_extract = zip_file_members[0]
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_file.extract(member=member_to_extract, path=temp_dir)
            df = pd.read_csv(Path(temp_dir) / member_to_extract)

        df = df[[StockColumns.SERIES, StockColumns.CLOSE]].drop_duplicates(subset=[StockColumns.SERIES])
        df = df.dropna(subset=[StockColumns.SERIES, StockColumns.CLOSE])
        df[StockColumns.DATE] = date

        logger.info(f"fetched {len(df)} sanitized records for {date}")
        return df

    @staticmethod
    def postgres_upsert(table, conn, keys, data_iter):
        """Custom postgres upsert method required to add on conflict do nothing clause"""
        from sqlalchemy.dialects.postgresql import insert

        data = [dict(zip(keys, row)) for row in data_iter]

        insert_statement = insert(table.table).values(data)
        upsert_statement = insert_statement.on_conflict_do_update(
            # constraint=f"series_date_unique_constraint",
            constraint=Stocks.__table_args__[0].name,
            set_={c.key: c for c in insert_statement.excluded},
        )
        result = conn.execute(upsert_statement)
        return result.rowcount

    def ingest(self, stocks: pd.DataFrame) -> None:
        """Ingest stocks to DB"""
        stocks = stocks.rename(columns={
            StockColumns.SERIES: Stocks.series.name,
            StockColumns.DATE: Stocks.date.name,
            StockColumns.CLOSE: Stocks.closing_price.name
        }).reset_index(drop=True)

        connection = self.engine.connect()
        trans = connection.begin()
        try:
            n_rows = stocks.to_sql(
                name=Stocks.__tablename__,
                con=connection,
                if_exists="append",
                index=False,
                method=self.postgres_upsert  # type: ignore
            )
            trans.commit()
            logger.info(f"inserted {n_rows} records to db")
        except Exception as e:
            trans.rollback()
            raise e

    def execute(self, start_date: str, end_date: str):
        """Entrypoint for Stock fetcher"""
        self.start_date = self.parse_date_format(start_date)
        self.end_date = self.parse_date_format(end_date)

        if self.start_date > self.end_date:
            logger.error("invalid input, start_date is ahead of end_date")
            return

        if self.start_date > datetime.datetime.now().date():
            logger.error("invalid input, start_date is in future")
            return

        date_list = [
            self.start_date + datetime.timedelta(days=day_count)
            for day_count in range((self.end_date - self.start_date).days + 1)
        ]

        for date_item in date_list:
            # execute fetch stocks
            stocks = self.fetch_stocks(date=date_item)
            self.ingest(stocks=stocks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        "--start_date",
        nargs="?",
        dest="start_date",
        help="Fetch records starting this date",
    )

    parser.add_argument(
        "--end_date",
        nargs="?",
        dest="end_date",
        help="Optional: end date default: current date",
        default=datetime.datetime.now().strftime("%d-%m-%Y")
    )

    arguments = parser.parse_args()
    logger.info(f"Fetching stocks for {arguments}")
    StockFetcher().execute(start_date=arguments.start_date, end_date=arguments.end_date)
    logger.info("Finished fetching all stocks")
