"""
Simple test for pytest
"""


def add(a: int | float, b: int | float) -> int | float:
    """
    a function that returns the sum of a and b
    :param a: an int or float
    :param b: an int or float
    :return: sum of a and b
    """
    return a + b


def test_add():
    assert add(1, 1) == 2
    assert add(0, 0) == 0
    assert add(1, 2) == 3
    assert add(1, -1) == 0
    assert add(1, -2) == -1
