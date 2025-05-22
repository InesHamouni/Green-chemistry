from unittest.mock import patch
from green_chemistry.picto import get_pictos

@patch("green_chemistry.picto.get_hazard_from_pugview_data")
def test_get_pictos_with_mocked_data(mock_get_hazard):
    # output API simulation
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
    assert "image1.svg" in result[0]
