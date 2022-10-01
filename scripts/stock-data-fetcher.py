# Fetch stocks from a BSE index
# Input:
#  end_date(Optional): Date time (DD-MM-YYYY)
#
#
# Command
# python stock-data-fetcher.py --end-date 20-09-2022

#

import argparse
import datetime
import io
import logging
import tempfile
import zipfile
from http import HTTPStatus
from pathlib import Path

import pandas as pd

import requests as requests

from scripts.constants import STOCK_URI, StockColumns, REQUIRED_STOCK_COLUMNS

logger = logging.getLogger(__name__)


class StockFetcher:

    def __init__(self):
        """init"""
        self.end_date = None
        self.start_date = None

    @staticmethod
    def parse_date_format(date: str) -> datetime.date:
        """"""
        try:
            parsed_date = datetime.datetime.strptime(date, "%d-%m-%Y").date()
            return parsed_date
        except ValueError as e:
            logger.error(e)
            raise Exception(f"Invalid date input {date}")

    @staticmethod
    def fetch_stocks(date: datetime.date) -> pd.DataFrame:
        """"""
        request_uri = STOCK_URI.format(
            date.strftime("%Y"),
            date.strftime("%b").upper(),
            date.strftime("%d"),
            date.strftime("%b").upper(),
            date.strftime("%Y")
        )

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
        df[StockColumns.DATE] = date

        return df

    def execute(self, start_date: str, end_date: str):
        """Entrypoint for Stock fetcher"""
        self.start_date = self.parse_date_format(start_date)
        self.end_date = self.parse_date_format(end_date)

        date_list = [
            self.start_date + datetime.timedelta(days=day_count)
            for day_count in range((self.end_date - self.start_date).days + 1)
        ]

        for date_item in date_list:
            # execute fetch stocks
            stocks = self.fetch_stocks(date=date_item)


if __name__ == "main":
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
    )

    arguments = parser.parse_args()
    logger.info(f"Fetching stocks for {arguments}")
    StockFetcher().execute(start_date=arguments.start_date, end_date=arguments.end_date)
    logger.info("Finished fetching all stocks")
