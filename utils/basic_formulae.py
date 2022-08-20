from functools import reduce
from collections.abc import Sequence
from collections import namedtuple

STOCK = namedtuple("STOCK", ["symbol", "stock_type", "last_dividend", "fixed_dividend", "par_value"])

def common_dividend_yield(last_dividend:float, price:float) -> float:
    """
    Base formula to collect common dividend yield

    :param last_dividend:
    :param price:

    :return:
    """
    try:
        result = last_dividend / price
    except ZeroDivisionError:
        raise Exception("Cannot have non-zero value for price")
    return result


def preferred_dividend_yield(fixed_dividend:float, par_value:float, price:float) -> float:
    """
    Base formula to collect preferred dividend yield

    :param fixed_dividend:
    :param par_value:
    :param price:

    :return:
    """
    try:
        result = (fixed_dividend * par_value) / price
    except ZeroDivisionError:
        raise Exception("Cannot have non-zero value for price")
    return result

def pe_ratio(dividend:float, price:float) -> float or str:
    """
    Base formula to collect pe ratio

    :param dividend:
    :param price:

    :return:
    """
    try:
        result = price / dividend
    except ZeroDivisionError:
        return "N/A"
    return result

def geometric_mean(args:Sequence[float]) -> float:
    """

    :param args: array of prices
    :return: geometric mean
    """
    result = product(args) ** (1/len(args))
    if isinstance(result,complex):
        raise Exception("Cannot take root of a negative product")
    return result

def product(args:Sequence[float]) -> float:
    """

    :param args:
    :return:
    """
    if not args:
        return 0
    prod = reduce(lambda x,y:x*y, args)
    return prod

def volume_weighted_stock_price(traded_price:Sequence[float], quantity:Sequence[int]) -> float:
    """

    :param traded_price:
    :param quantity:
    :return:
    """
    traded_price_sum = sum(traded_price)
    non_int_quantities = list(filter(lambda x: not isinstance(x,int), quantity))
    if len(non_int_quantities) > 0:
        raise Exception("Quantity has to be integer values")
    quantity_sum = sum(quantity)
    last_quantity = quantity[-1] if len(quantity) > 0 else 0

    try:
        result = (traded_price_sum * last_quantity) / quantity_sum
    except ZeroDivisionError:
        raise Exception("Sum of Quantity cannot be 0")
    return result
