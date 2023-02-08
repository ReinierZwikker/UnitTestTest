from ISA_Calculator import *
import pytest


def test_unit_converters():
    assert temperature_kelvin_to_celsius(0) == -273.15
    assert temperature_celsius_to_kelvin(0) == 273.15
    assert correct_units(10, 1) == 15
    assert correct_units(10, 2) == 10 / 3.281
    assert correct_units(10, 2) != 10
    assert correct_units(10, 3) != 10
    assert correct_units(10, 3) == 1000 / 3.281


@pytest.mark.parametrize("test_value,test_ceiling,expected_result", [(10, 20, 10), (30, 20, 20), (20, 20, 20), (-5, 20, -5),
                                                                     (-10, -20, -20), (20, 10, 10)])
def test_ceiling_function(test_value, test_ceiling, expected_result):
    assert ceiling(test_value, test_ceiling) == expected_result


@pytest.mark.parametrize("test_height,expected_result", [(1, (101312.985, 288.143, 1.22511)), (85999, (0.302, 184.652, 1e-05))])
def test_calculate_isa(test_height, expected_result):
    assert calculate_isa(test_height) == expected_result


@pytest.mark.parametrize("test_height", [-1, 0, 86001])
def test_calculate_isa_height(test_height):
    with pytest.raises(HeightError):
        calculate_isa(test_height)
