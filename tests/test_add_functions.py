import streamlit as st
from unittest.mock import patch
from green_chemistry.script_interface import (
    query_pubchem_api,
    add_compound,
    add_product,
    add_solvents,
    add_catalyzer
)

mock_data = {
    "MolecularFormula": "H2O",
    "MolecularWeight": 18.02,
    "Title": "Water"
}

@patch("green_chemistry.script_interface.query_pubchem_api", return_value=mock_data)
@patch("green_chemistry.script_interface.st.success")
@patch("green_chemistry.script_interface.st.error")
def test_add_compound(mock_error, mock_success, mock_query):
    st.session_state.compounds = []
    add_compound("water")
    assert len(st.session_state.compounds) == 1

@patch("green_chemistry.script_interface.query_pubchem_api", return_value=mock_data)
@patch("green_chemistry.script_interface.st.success")
@patch("green_chemistry.script_interface.st.error")
def test_add_product(mock_error, mock_success, mock_query):
    st.session_state.product = []
    add_product("salt")
    assert len(st.session_state.product) == 1

@patch("green_chemistry.script_interface.query_pubchem_api", return_value=mock_data)
@patch("green_chemistry.script_interface.st.success")
@patch("green_chemistry.script_interface.st.error")
def test_add_solvents(mock_error, mock_success, mock_query):
    st.session_state.solvents = []
    add_solvents("ethanol")
    assert len(st.session_state.solvents) == 1

@patch("green_chemistry.script_interface.query_pubchem_api", return_value=mock_data)
@patch("green_chemistry.script_interface.st.success")
@patch("green_chemistry.script_interface.st.error")
def test_add_catalyzer(mock_error, mock_success, mock_query):
    st.session_state.catalyzer = []
    add_catalyzer("Pd")
    assert len(st.session_state.catalyzer) == 1
