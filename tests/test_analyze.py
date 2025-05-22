from unittest.mock import patch
import streamlit as st
from green_chemistry.script_interface import analyze

@patch("green_chemistry.script_interface.get_pictos")
@patch("green_chemistry.script_interface.pressure_efficiency")
@patch("green_chemistry.script_interface.temperature_efficiency")
@patch("green_chemistry.script_interface.get_metal_impact")
@patch("green_chemistry.script_interface.atom_economy")
def test_analyze_returns_expected_dict(mock_atom_econ, mock_metal, mock_temp, mock_press, mock_pictos):
    # Mock of functions
    mock_atom_econ.return_value = (85.0, "Good")
    mock_metal.return_value = "MetalName\nToxicity: Low\nAvailability: High"
    mock_temp.return_value = "Low temperature"
    mock_press.return_value = "Low pressure"
    mock_pictos.return_value = ["https://example.com/picto1.svg"]

    # session state
    st.session_state.compounds = [{"MolecularWeight": 100, "Title": "Reactant"}]
    st.session_state.product = [{"MolecularWeight": 200, "Title": "Product"}]
    st.session_state.solvents = [{"Title": "Water"}]
    st.session_state.catalyzer = [{"MolecularFormula": "Pd", "Title": "Palladium"}]
    st.session_state.temperature = 25
    st.session_state.pressure = 1

    result = analyze()

    assert isinstance(result, dict)
    assert "atom_economy" in result
    assert "metal_analysis" in result
    assert "temperature_efficiency" in result
    assert "pressure_efficiency" in result
    assert "compounds_pictos" in result
    assert "products_pictos" in result
    assert "solvents_pictos" in result
    assert "catalyzers_pictos" in result
