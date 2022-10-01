STOCK_URI = "https://www1.nseindia.com/content/historical/EQUITIES/2022/SEP/cm01SEP2022bhav.csv.zip"


class StockColumns:
    SERIES = "series"
    CLOSE = "close"
    DATE = "date"


REQUIRED_STOCK_COLUMNS = [StockColumns.SERIES, StockColumns.CLOSE, StockColumns.DATE]
