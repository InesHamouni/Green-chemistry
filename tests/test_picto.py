import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# test functions to extract the pictograms for each compound from PubChem

from green_chemistry.picto import get_hazard_from_pugview_data, extract_pictogram_urls, get_pictos

def test_get_hazard_from_pugview_data():
    """ the lead is taken as the compound example"""

    data = get_hazard_from_pugview_data("lead")
    assert isinstance(data, list) or 'Error' in data

def test_extract_pictogram_urls():
    """ The Markup has been simplified for the test function and only the URL has been conserved"""
    
    sample_data = [{
        "Markup": [
            {"URL": "https://pubchem.ncbi.nlm.nih.gov/images/ghs/GHS08.svg"},
            {"URL": "https://pubchem.ncbi.nlm.nih.gov/images/ghs/GHS09.svg"}
        ]
    }]
    urls = extract_pictogram_urls(sample_data)
    assert isinstance(urls, list)
    assert "https://pubchem.ncbi.nlm.nih.gov/images/ghs/GHS08.svg" in urls

def test_get_pictos():
    urls = get_pictos("lead")
    assert isinstance(urls, list)
    assert all(url.startswith("https://") for url in urls) or len(urls) == 0
