"""Unit tests cho module app/calc.py su dung pytest."""
import pytest
from app.calc import add, sub, mul, div, pow, sqrt

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_sub():
    assert sub(10, 4) == 6
    assert sub(3, 5) == -2
    assert sub(0, 0) == 0

def test_mul():
    assert mul(3, 4) == 12
    assert mul(-2, 5) == -10
    assert mul(0, 100) == 0

def test_div():
    assert div(10, 2) == 5
    assert div(7, 2) == 3.5

def test_div_by_zero():
    with pytest.raises(ZeroDivisionError, match="ZeroDivision"):
        div(1, 0)

def test_pow():
    assert pow(2, 3) == 8
    assert pow(5, 0) == 1
    assert pow(2, -1) == 0.5

def test_sqrt():
    assert sqrt(9) == 3
    assert sqrt(0) == 0

def test_sqrt_negative():
    with pytest.raises(ValueError, match="Khong the tinh can so am"):
        sqrt(-4)
