import re
from utils.basic_formulae import *
from datetime import datetime, timedelta

class TRADE:
    def __init__(self, timestamp:datetime or float,
                 quantity:int or float,
                 indicator:str,
                 price:float):
        if isinstance(timestamp, datetime):
            self.timestamp = timestamp
        elif isinstance(timestamp, float) or isinstance(timestamp, int):
            self.timestamp = datetime.fromtimestamp(timestamp)

        if not (isinstance(quantity,int) or isinstance(quantity,float)):
            raise Exception("Quantity has to be a number")
        if quantity < 0:
            raise Exception("Quantity cannot be negative")
        self.quantity = quantity

        if indicator.upper() not in ("BUY","SELL"):
            raise Exception("Indicator has to be BUY or SELL")
        self.indicator = indicator.upper()

        if not (isinstance(price,float) or isinstance(price,int)):
            raise Exception("Price has to be a number")
        if price < 0:
            raise Exception("Price cannot be negative")
        self.price = price

    def __str__(self):
        display_string = f"{self.timestamp.timestamp()},{self.quantity},{self.indicator},{self.price}"
        return display_string


class STOCK:
    def __init__(self, symbol:str or None = None,
                 stock_type:str or None = None,
                 last_dividend:float or None = None,
                 fixed_dividend:float or None = None,
                 par_value:float or None = None):
        if symbol is None:
            raise Exception("Stock Symbol cannot be empty")
        symbol_format = re.match("^[A-Z]{3}$",symbol)
        if not symbol_format:
            raise Exception("Invalid Stock Symbol. Has to be of format AAA all in uppercase")
        self.symbol = symbol

        if stock_type.upper() not in ("COMMON", "PREFERRED"):
            raise Exception("Stock Type has to be either COMMON or PREFERRED")
        self.stock_type = stock_type.upper()
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend
        self.par_value = par_value

        self.trades = []

    def dividend_yield(self, price):
        if self.stock_type == "COMMON":
            return common_dividend_yield(last_dividend=self.last_dividend, price=price)
        elif self.stock_type == "PREFERRED":
            return preferred_dividend_yield(fixed_dividend=self.fixed_dividend, par_value=self.par_value, price=price)

    def pe_ratio(self, price):
        return pe_ratio(dividend=self.last_dividend, price=price)

    def record_trade(self, timestamp, quantity, indicator, price):
        self.trades.append(TRADE(timestamp=timestamp, quantity=quantity,indicator=indicator,price=price))

    def volume_weighted_stock_price(self):
        base = datetime.now()
        last_15min_trades = [x for x in self.trades if x.timestamp > (base - timedelta(minutes=15))]
        last_15min_trades = sorted(last_15min_trades, key=lambda x: x.timestamp)
        traded_price_last_15_min = [x.price for x in last_15min_trades]
        quantity_last_15_min = [x.quantity for x in last_15min_trades]
        return volume_weighted_stock_price(traded_price=traded_price_last_15_min, quantity=quantity_last_15_min)

    def product(self):
        return product([x.price for x in self.trades])

    def count_trades(self):
        return len(self.trades)

    def __str__(self):
        display_string = f"\n{self.symbol}, {self.stock_type}, {self.last_dividend}, {self.fixed_dividend}, {self.par_value}"
        display_string += f"\nTrades (Timestamp, Quantity, Type, Price)"
        for i in self.trades:
            display_string += f"\n{i}"
        return display_string

class AllShareIndex:
    def __init__(self, stocks:Sequence[STOCK]):
        invalid_stocks = list(filter(lambda x: not isinstance(x,STOCK),stocks))
        if invalid_stocks:
            raise Exception("Stocks Iterable has to be of type STOCK")
        self.stocks = stocks

    def __len__(self):
        return len(self.stocks)

    def __getitem__(self, item:str):
        match = list(filter(lambda x: x.symbol == item.upper(),self.stocks))
        if len(match) == 1:
            return match[0]
        elif len(match) > 1:
            return match
        elif len(match) == 0:
            raise Exception(f"Stock {item} does not exist")

    def all_share_index(self):
        mean = 1
        number_of_prices = 0
        for stock in self.stocks:
            mean *= stock.product()
            number_of_prices += stock.count_trades()
        return mean ** (1/number_of_prices)

