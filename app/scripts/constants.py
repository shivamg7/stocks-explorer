STOCK_URI = "https://www1.nseindia.com/content/historical/EQUITIES/{}/{}/cm{}{}{}bhav.csv.zip"


class StockColumns:
    SYMBOL = "SYMBOL"
    SERIES = "SERIES"
    CLOSE = "CLOSE"
    DATE = "DATE"


REQUIRED_STOCK_COLUMNS = [StockColumns.SERIES, StockColumns.CLOSE, StockColumns.DATE]
