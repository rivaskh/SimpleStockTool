from utils.basic_formulae import *
import unittest

class TestCommonDividendYield(unittest.TestCase):
    def test_validresult_1(self):
        result = common_dividend_yield(last_dividend=0,price=1)
        self.assertEqual(result,0,"Got an incorrect value for common dividend yield")

    def test_validresult_2(self):
        result = common_dividend_yield(last_dividend=24,price=1)
        self.assertEqual(result,24,"Got an incorrect value for common dividend yield")

    def test_validresult_3(self):
        result = common_dividend_yield(last_dividend=24.00,price=1.00)
        self.assertEqual(result,24.00,"Got an incorrect value for common dividend yield")

    def test_divide_by_0(self):
        with self.assertRaises(Exception) as context:
            common_dividend_yield(last_dividend=24,price=0)
        self.assertTrue("Cannot have non-zero value for price" in str(context.exception))

    def test_string_arguments(self):
        with self.assertRaises(TypeError) as context:
            common_dividend_yield(last_dividend="24",price=1)

        with self.assertRaises(TypeError) as context:
            common_dividend_yield(last_dividend=24,price="1")

class TestPreferredDividendYield(unittest.TestCase):
    def test_validresult_1(self):
        result = preferred_dividend_yield(fixed_dividend=0,par_value=1,price=1)
        self.assertEqual(result,0,"Got an incorrect value for preferred dividend yield")

    def test_validresult_2(self):
        result = preferred_dividend_yield(fixed_dividend=10,par_value=10,price=1)
        self.assertEqual(result,100,"Got an incorrect value for preferred dividend yield")

    def test_validresult_3(self):
        result = preferred_dividend_yield(fixed_dividend=10.00,par_value=10.00,price=2.00)
        self.assertEqual(result,50,"Got an incorrect value for preferred dividend yield")

    def test_validresult_4(self):
        result = preferred_dividend_yield(fixed_dividend=10,par_value=10,price=2)
        self.assertEqual(result,50,"Got an incorrect value for preferred dividend yield")

    def test_divide_by_0(self):
        with self.assertRaises(Exception) as context:
            preferred_dividend_yield(fixed_dividend=10,par_value=10,price=0)
        self.assertTrue("Cannot have non-zero value for price" in str(context.exception))

    def test_string_arguments(self):
        with self.assertRaises(TypeError) as context:
            preferred_dividend_yield(fixed_dividend="10",par_value=10,price=1.00)

        with self.assertRaises(TypeError) as context:
            preferred_dividend_yield(fixed_dividend=10,par_value="10",price=1.00)

        with self.assertRaises(TypeError) as context:
            preferred_dividend_yield(fixed_dividend=10,par_value=10,price="1.00")

class TestPERatio(unittest.TestCase):
    def test_validresult_1(self):
        result = pe_ratio(dividend=1,price=0)
        self.assertEqual(result,0,"Got an incorrect value for pe ratio")

    def test_validresult_2(self):
        result = pe_ratio(dividend=1,price=10)
        self.assertEqual(result,10,"Got an incorrect value for pe ratio")

    def test_validresult_3(self):
        result = pe_ratio(dividend=2,price=10)
        self.assertEqual(result,5,"Got an incorrect value for pe ratio")

    def test_divide_by_0(self):
        result = pe_ratio(dividend=0,price=10)
        self.assertEqual(result,"N/A")

def test_string_arguments(self):
        with self.assertRaises(TypeError) as context:
            pe_ratio(dividend="10",price=10)

        with self.assertRaises(TypeError) as context:
            pe_ratio(price="10",dividend=10)

class TestGeometricMean(unittest.TestCase):
    def test_validresult_1(self):
        result = geometric_mean([3,3])
        self.assertEqual(result,3,"Got an incorrect value for geometric mean")

    def test_validresult_2(self):
        result = geometric_mean([10,2,3,4])
        self.assertEqual(result,240**(1/4),"Got an incorrect value for geometric mean")

    def test_validresult_3(self):
        result = geometric_mean([1.0, 2, 2, 4.00, 4])
        self.assertEqual(result,64**(1/5),"Got an incorrect value for geometric mean")

    def test_validresult_4(self):
        result = geometric_mean([-1.0, 2, -2, 4.00, 4])
        self.assertEqual(result,64**(1/5),"Got an incorrect value for geometric mean")

    def test_string_arguments(self):
        with self.assertRaises(TypeError) as context:
            geometric_mean([1,"2",3])

    def test_negative_product(self):
        with self.assertRaises(Exception) as context:
            result = geometric_mean([-1, 3])
        self.assertTrue("Cannot take root of a negative product" in str(context.exception))

class TestVolumeWeightedStockPrice(unittest.TestCase):
    def test_validresult_1(self):
        result = volume_weighted_stock_price(traded_price=(1,2,3), quantity=(1,1,1))
        self.assertEqual(result,2,"Got an incorrect value for Volume Weighted Stock Price")

    def test_validresult_2(self):
        result = volume_weighted_stock_price(traded_price=(1.00,2.00,3.00), quantity=(1,1,1))
        self.assertEqual(result,2.00,"Got an incorrect value for Volume Weighted Stock Price")

    def test_validresult_3(self):
        result = volume_weighted_stock_price(traded_price=(0,0,0), quantity=(1,1,1))
        self.assertEqual(result,0,"Got an incorrect value for Volume Weighted Stock Price")

    def test_float_arguments_for_quantity(self):
        with self.assertRaises(Exception) as context:
            volume_weighted_stock_price(traded_price=(1.00,2.00,3.00), quantity=(1.00,1.00,1.02))
        self.assertTrue("Quantity has to be integer values" in str(context.exception))

    def test_sum_quantity_is_0(self):
        with self.assertRaises(Exception) as context:
            volume_weighted_stock_price(traded_price=(1.00,2.00,3.00), quantity=(1,1,-2))
        self.assertTrue("Sum of Quantity cannot be 0" in str(context.exception))

    def test_string_arguments(self):
        with self.assertRaises(TypeError) as context:
            volume_weighted_stock_price(1,"2",3)

if __name__ == "__main__":
    unittest.main()
