from yf_service.stats.aus.aus_stock_class import AusStockClass
from yf_service.stats.us.us_stock_class import US_StockClass


class StockController:
    def __init__(self, code: str, country: str):
        if country.lower() == "aus":
            self.si = AusStockClass(ticker=code)

        elif country.lower() == "us":
            self.si = US_StockClass(ticker=code)
