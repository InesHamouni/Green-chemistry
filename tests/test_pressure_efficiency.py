import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from green_chemistry.pressure_efficiency import pressure_efficiency

def test_atmospheric_pressure():
    assert pressure_efficiency(1) == "atmospheric pressure, zero energy consumption"

def test_low_pressure():
    assert pressure_efficiency(2) == "low energy consumption"
    assert pressure_efficiency(4.9) == "low energy consumption"

def test_moderate_pressure():
    assert pressure_efficiency(5) == "moderate energy consumption"
    assert pressure_efficiency(29.9) == "moderate energy consumption"

def test_high_pressure():
    assert pressure_efficiency(30) == "high energy consumption"
    assert pressure_efficiency(50) == "high energy consumption"

def test_boundary_conditions():
    assert pressure_efficiency(1.0001) == "low energy consumption"
    assert pressure_efficiency(5.0) == "moderate energy consumption"
