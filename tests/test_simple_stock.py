import unittest
from utils.stock import STOCK, TRADE, AllShareIndex
from datetime import datetime, timedelta

class TestStock(unittest.TestCase):
    def test_assign_valid_1(self):
        s1 = STOCK(symbol="TEA", stock_type="COMMON", last_dividend=0, par_value=100)
        self.assertTrue(s1)

    def test_assign_valid_2(self):
        s1 = STOCK(symbol="GIN", stock_type="PREFERRED", last_dividend=8, fixed_dividend=2, par_value=60)
        self.assertTrue(s1)

    def test_assign_valid_3(self):
        s1 = STOCK(symbol="GIN", stock_type="preFeRred", last_dividend=8, fixed_dividend=2, par_value=60)
        self.assertTrue(s1)

    def test_assign_invalid_type(self):
        with self.assertRaises(Exception) as context:
            s1 = STOCK(symbol="GIN", stock_type="INVALID", last_dividend=8, fixed_dividend=2, par_value=60)
        self.assertTrue("Stock Type has to be either COMMON or PREFERRED" in str(context.exception))

    def test_assign_empty_symbol(self):
        with self.assertRaises(Exception) as context:
            s1 = STOCK(stock_type="COMMON", last_dividend=8, fixed_dividend=2, par_value=60)
        self.assertTrue("Stock Symbol cannot be empty" in str(context.exception))

    def test_assign_invalid_symbol_1(self):
        with self.assertRaises(Exception) as context:
            s1 = STOCK(symbol=1, stock_type="COMMON", last_dividend=8, fixed_dividend=2, par_value=60)
        self.assertTrue("Invalid Stock Symbol. Has to be of format AAA all in uppercase")

    def test_assign_invalid_symbol_2(self):
        with self.assertRaises(Exception) as context:
            s1 = STOCK(symbol="ABCD", stock_type="COMMON", last_dividend=8, fixed_dividend=2, par_value=60)
        self.assertTrue("Invalid Stock Symbol. Has to be of format AAA all in uppercase")

    def test_product(self):
        s1 = STOCK(symbol="TEA", stock_type="COMMON", last_dividend=0, par_value=100)
        s1.record_trade(
            timestamp=datetime.now() - timedelta(minutes=5),
            quantity=10,
            indicator="buy",
            price=100
        )
        s1.record_trade(
            timestamp=datetime.now() - timedelta(minutes=4),
            quantity=20,
            indicator="sell",
            price=100
        )
        mean = s1.product()
        self.assertEqual(mean,10000,"Expected value of 100")

    def test_geometric_mean_with_no_trades(self):
        s1 = STOCK(symbol="TEA", stock_type="COMMON", last_dividend=0, par_value=100)
        mean = s1.product()
        self.assertEqual(mean,0,"Expected value of 0")

class TestTrade(unittest.TestCase):
    def test_valid_1(self):
        ts = datetime(day=1,month=1,year=2022,hour=1,second=30,microsecond=500)
        a = TRADE(timestamp=ts, quantity=10, indicator="buy", price=100)
        self.assertEqual(a.timestamp, datetime(day=1,month=1,year=2022,hour=1,second=30,microsecond=500))

    def test_valid_2(self):
        ts = 1640979030.0005
        a = TRADE(timestamp=ts, quantity=10, indicator="buy", price=100)
        self.assertEqual(a.timestamp, datetime(day=1,month=1,year=2022,hour=1,second=30,microsecond=500))

    def test_valid_3(self):
        ts = 1640979030
        a = TRADE(timestamp=ts, quantity=10, indicator="buy", price=100)
        self.assertEqual(a.timestamp, datetime(day=1,month=1,year=2022,hour=1,second=30))

    def test_no_timestamp(self):
        with self.assertRaises(TypeError) as context:
            TRADE(quantity=10, indicator="buy", price=100)

    def test_no_quantity(self):
        ts = 1640979030
        with self.assertRaises(TypeError) as context:
            TRADE(timestamp=ts, indicator="buy", price=100)

    def test_no_indicator(self):
        ts = 1640979030
        with self.assertRaises(TypeError) as context:
            TRADE(timestamp=ts, quantity=1, price=100)

    def test_no_price(self):
        ts = 1640979030
        with self.assertRaises(TypeError) as context:
            TRADE(timestamp=ts, quantity=1, indicator="buy")

    def test_quantity_is_string(self):
        ts = 1640979030
        with self.assertRaises(Exception) as context:
            TRADE(timestamp=ts, quantity="1", indicator="buy", price=100)
        self.assertTrue("Quantity has to be a number" in str(context.exception))

    def test_quantity_cannot_be_negative(self):
        ts = 1640979030
        with self.assertRaises(Exception) as context:
            TRADE(timestamp=ts, quantity=-1, indicator="buy", price=100)
        self.assertTrue("Quantity cannot be negative" in str(context.exception))

    def test_invalid_value_of_indicator(self):
        ts = 1640979030
        with self.assertRaises(Exception) as context:
            TRADE(timestamp=ts, quantity=1, indicator="INVALID", price=100)
        self.assertTrue("Indicator has to be BUY or SELL" in str(context.exception))

    def test_invalid_value_of_price_1(self):
        ts = 1640979030
        with self.assertRaises(Exception) as context:
            TRADE(timestamp=ts, quantity=1, indicator="BUY", price="INVALID")

    def test_price_is_string(self):
        ts = 1640979030
        with self.assertRaises(Exception) as context:
            TRADE(timestamp=ts, quantity=1, indicator="buy", price="100")
        self.assertTrue("Price has to be a number" in str(context.exception))

    def test_price_cannot_be_negative(self):
        ts = 1640979030
        with self.assertRaises(Exception) as context:
            TRADE(timestamp=ts, quantity=1, indicator="buy", price=-100)
        self.assertTrue("Price cannot be negative" in str(context.exception))

class TestAllShareIndex(unittest.TestCase):
    def test_assign_valid_1(self):
        allshareindex = AllShareIndex([
            STOCK(symbol="TEA", stock_type="COMMON", last_dividend=0, par_value=100),
            STOCK(symbol="POP", stock_type="COMMON", last_dividend=8, par_value=100),
        ])
        self.assertTrue(allshareindex)
        self.assertEqual(len(allshareindex), 2, "Expected a length of two shares")

    def test_invalid_sequence_of_stocks(self):
        with self.assertRaises(Exception) as context:
            allshareindex = AllShareIndex([
                ("TEA", "COMMON", 0, 100),
                ("POP", "COMMON", 8, 100),
            ])
        self.assertTrue("Stocks Iterable has to be of type STOCK" in str(context.exception))

    def test_find_specific_stock(self):
        allshareindex = AllShareIndex([
            STOCK(symbol="TEA", stock_type="COMMON", last_dividend=0, par_value=100),
            STOCK(symbol="POP", stock_type="COMMON", last_dividend=8, par_value=100),
        ])
        self.assertEqual(allshareindex["TEA"].last_dividend, 0, "Expected last dividend value to be 0")
        self.assertEqual(allshareindex["POP"].last_dividend, 8, "Expected last dividend value to be 8")

    def test_find_group_of_stocks(self):
        allshareindex = AllShareIndex([
            STOCK(symbol="TEA", stock_type="COMMON", last_dividend=0, par_value=100),
            STOCK(symbol="TEA", stock_type="COMMON", last_dividend=0, par_value=100),
            STOCK(symbol="POP", stock_type="COMMON", last_dividend=8, par_value=100),
        ])
        self.assertEqual(len(allshareindex["TEA"]), 2, "Expected two values present")

    def test_non_existing_stock(self):
        allshareindex = AllShareIndex([
            STOCK(symbol="TEA", stock_type="COMMON", last_dividend=0, par_value=100),
            STOCK(symbol="POP", stock_type="COMMON", last_dividend=8, par_value=100),
        ])
        with self.assertRaises(Exception) as context:
            nonexisting = allshareindex["JOE"]
        self.assertTrue("Stock JOE does not exist" in str(context.exception))
