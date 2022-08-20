"""
For a given stock,
    i. Given any price as input, calculate the dividend yield
    ii. Given any price as input, calculate the P/E Ratio
    iii. Record a trade, with timestamp, quantity of shares, buy or sell indicator and traded price
    iv. Calculate Volume Weighted Stock Price based on trades in past 15 minutes

Calculate the GBCE All Share Index using the geometric mean of prices for all stocks
"""
import datetime

from utils.stock import STOCK, AllShareIndex


########## CREATION OF GBCE SHARE UNITS ##########
sample_data = [
    STOCK(symbol="TEA", stock_type="COMMON", last_dividend=0, par_value=100),
    STOCK(symbol="POP", stock_type="COMMON", last_dividend=8, par_value=100),
    STOCK(symbol="ALE", stock_type="COMMON", last_dividend=23, par_value=60),
    STOCK(symbol="GIN", stock_type="PREFERRED", last_dividend=8, fixed_dividend=2, par_value=60),
    STOCK(symbol="JOE", stock_type="COMMON", last_dividend=13, par_value=250),
]
GBCE = AllShareIndex(sample_data)


########## SOME HELPER FUNCTIONS ##########
def shifted_date(minutes:int) -> datetime.datetime:
    return datetime.datetime.now() - datetime.timedelta(minutes=minutes)

def calculate_metrics_of_stock(stock_name, price):
    metrics = {
        "dividend_yield":GBCE[stock_name].dividend_yield(price=price),
        "PE_ratio":GBCE[stock_name].pe_ratio(price=price),
        "Volume Weighted Stock Price":GBCE[stock_name].volume_weighted_stock_price()
    }
    print (metrics)


########## RECORDING OF TRADES (RANDOMLY ADDED) ##########
GBCE["TEA"].record_trade(timestamp=shifted_date(minutes=1), quantity=1, indicator="BUY", price=1000)
GBCE["POP"].record_trade(timestamp=shifted_date(minutes=2), quantity=5, indicator="SELL", price=200)
GBCE["POP"].record_trade(timestamp=shifted_date(minutes=3), quantity=10, indicator="BUY", price=553)
GBCE["JOE"].record_trade(timestamp=shifted_date(minutes=3), quantity=100, indicator="BUY", price=27)
GBCE["POP"].record_trade(timestamp=shifted_date(minutes=4), quantity=2, indicator="SELL", price=1000)
GBCE["TEA"].record_trade(timestamp=shifted_date(minutes=5), quantity=101, indicator="BUY", price=2000)
GBCE["POP"].record_trade(timestamp=shifted_date(minutes=6), quantity=100, indicator="BUY", price=30)
GBCE["TEA"].record_trade(timestamp=shifted_date(minutes=6), quantity=11, indicator="BUY", price=40)
GBCE["ALE"].record_trade(timestamp=shifted_date(minutes=9), quantity=5, indicator="SELL", price=80)
GBCE["ALE"].record_trade(timestamp=shifted_date(minutes=10), quantity=6, indicator="SELL", price=100)
GBCE["ALE"].record_trade(timestamp=shifted_date(minutes=11), quantity=1, indicator="SELL", price=90)
GBCE["ALE"].record_trade(timestamp=shifted_date(minutes=11), quantity=3, indicator="BUY", price=80)
GBCE["ALE"].record_trade(timestamp=shifted_date(minutes=12), quantity=5, indicator="BUY", price=10)
GBCE["GIN"].record_trade(timestamp=shifted_date(minutes=13), quantity=7, indicator="BUY", price=20)
GBCE["JOE"].record_trade(timestamp=shifted_date(minutes=16), quantity=8, indicator="SELL", price=30)
GBCE["GIN"].record_trade(timestamp=shifted_date(minutes=17), quantity=9, indicator="BUY", price=50)
GBCE["POP"].record_trade(timestamp=shifted_date(minutes=18), quantity=10, indicator="SELL", price=80)
GBCE["JOE"].record_trade(timestamp=shifted_date(minutes=21), quantity=11, indicator="BUY", price=90)
GBCE["ALE"].record_trade(timestamp=shifted_date(minutes=30), quantity=1, indicator="BUY", price=100)


########## DISPLAYING THE RESULTS ##########
print (GBCE["TEA"])
calculate_metrics_of_stock("TEA", 80)
print (GBCE["POP"])
calculate_metrics_of_stock("POP", 80)
print (GBCE["ALE"])
calculate_metrics_of_stock("ALE", 80)
print (GBCE["GIN"])
calculate_metrics_of_stock("GIN", 80)
print (GBCE["JOE"])
calculate_metrics_of_stock("JOE", 80)

print (f"\nGBCE All Share Index: {GBCE.all_share_index()}")