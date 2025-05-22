import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from green_chemistry.pressure_efficiency import pressure_efficiency

def test_pressure_efficiency_zero():
    result = pressure_efficiency(1)
    assert result == "atmospheric pressure, zero energy consumption"

def test_pressure_efficiency_low():
    result = pressure_efficiency(3)
    assert result == "low energy consumption"

def test_pressure_efficiency_moderate():
    result = pressure_efficiency(15)
    assert result == "moderate energy consumption"

def test_pressure_efficiency_high():
    result = pressure_efficiency(40)
    assert result == "high energy consumption"