import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from green_chemistry.metal_center import get_metal_impact

@pytest.mark.parametrize("metal, expected_substrings", [
    ("Pd", ["Palladium", "Moderate", "bioaccumulation", "Rare"]),
    ("Fe", ["Iron", "Low", "minimal", "abundant"]),
    ("Os", ["Osmium", "highly toxic", "aquatic life", "Extremely rare"]),
    ("Xx", ["No data available for Xx"]),
])
def test_get_metal_impact(metal, expected_substrings):
    result = get_metal_impact(metal)
    for substring in expected_substrings:
        assert substring in result
