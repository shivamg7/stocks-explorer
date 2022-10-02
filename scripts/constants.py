STOCK_URI = "https://www1.nseindia.com/content/historical/EQUITIES/2022/SEP/cm01SEP2022bhav.csv.zip"


class StockColumns:
    SERIES = "SERIES"
    CLOSE = "CLOSE"
    DATE = "DATE"


REQUIRED_STOCK_COLUMNS = [StockColumns.SERIES, StockColumns.CLOSE, StockColumns.DATE]
