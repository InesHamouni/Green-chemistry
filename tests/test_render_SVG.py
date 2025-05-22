from green_chemistry.convert_pictograms import render_svg
from unittest.mock import patch, Mock
import streamlit as st

@patch("green_chemistry.convert_pictograms.st.write")
@patch("green_chemistry.convert_pictograms.requests.get")
def test_render_svg(mock_get, mock_write):
    # Mock a valid SVG response
    mock_response = Mock()
    mock_response.content = b"<svg>MockSVG</svg>"
    mock_get.return_value = mock_response

    # Call the function with a mock URL
    render_svg(["http://example.com/image.svg"])

    # Check if the HTTP GET request was called with the correct URL
    mock_get.assert_called_once_with("http://example.com/image.svg")

    # Check if Streamlit wrote the HTML image to the app
    assert mock_write.called
