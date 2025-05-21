import sys
import os 
import base64

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# test render function

from green_chemistry.convert_pictograms import render_svg

def test_render_svg_multiple_urls():
    urls = [
        "https://pubchem.ncbi.nlm.nih.gov/images/ghs/GHS08.svg",
        "https://pubchem.ncbi.nlm.nih.gov/images/ghs/GHS09.svg",
        "https://pubchem.ncbi.nlm.nih.gov/images/ghs/GHS07.svg"
    ]
    
    html = render_svg(urls)

    # html must not be empty
    assert html is not None
    assert html.strip() != ""

    # must contain <img> with base64 SVG encoding
    assert html.startswith("<img")
    assert "data:image/svg+xml;base64," in html

    # check that the encoded image contains a <svg> tag when decoding
    b64_data = html.split("base64,")[1].split('"')[0]
    decoded_svg = base64.b64decode(b64_data).decode("utf-8")
    assert "<svg" in decoded_svg
    assert "</svg>" in decoded_svg


