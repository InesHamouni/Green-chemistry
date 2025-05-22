import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from green_chemistry.metal_center import get_metal_impact

def test_known_metal_output_format():
    """Test that a known metal returns a formatted string with expected keywords."""
    result = get_metal_impact("Pt")
    assert isinstance(result, str)
    assert "Platinum" in result
    assert "**Human toxicity**" in result
    assert "**Environmental impact**" in result
    assert "**Availability**" in result

def test_unknown_metal():
    """Test that an unknown metal returns the correct fallback message."""
    result = get_metal_impact("Xx")
    assert result == "No data available for Xx"