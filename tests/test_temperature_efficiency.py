import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from green_chemistry.temperature_efficiency import temperature_efficiency

def test_low_temperature():
    result = temperature_efficiency(25)
    assert result == "low energy consumption"

def test_moderate_temperature():
    result = temperature_efficiency(150)
    assert result == "moderate energy consumption"

def test_high_temperature():
    result = temperature_efficiency(250)
    assert result == "high energy consumption"

def test_boundary_values():
    assert temperature_efficiency(100) == "moderate energy consumption"
    assert temperature_efficiency(199.9) == "moderate energy consumption"
    assert temperature_efficiency(200) == "high energy consumption"
