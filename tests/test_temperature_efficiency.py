import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from green_chemistry.temperature_efficiency import temperature_efficiency

def test_temperature_efficiency_high():
    result = temperature_efficiency(250)
    assert result == "high energy consumption"

def test_temperature_efficiency_moderate():
    result = temperature_efficiency(150)
    assert result == "moderate energy consumption"

def test_temperature_efficiency_low():
    result = temperature_efficiency(50)
    assert result == "low energy consumption"
