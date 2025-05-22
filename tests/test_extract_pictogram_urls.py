from green_chemistry.picto import get_pictos
from unittest.mock import patch

@patch("green_chemistry.picto.get_hazard_from_pugview_data")
def test_get_pictos_with_mocked_data(mock_get_hazard):
    # Simulated API output
    mock_get_hazard.return_value = [
        {
            "Markup": [
                {"URL": "https://pubchem.ncbi.nlm.nih.gov/image1.svg"},
                {"URL": "https://pubchem.ncbi.nlm.nih.gov/image2.svg"},
            ]
        }
    ]

    result = get_pictos("fakecompound")
    assert isinstance(result, list)
    assert len(result) == 2
    assert "https://pubchem.ncbi.nlm.nih.gov/image1.svg" in result
    assert "https://pubchem.ncbi.nlm.nih.gov/image2.svg" in result

