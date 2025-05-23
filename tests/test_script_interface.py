import sys
import os 
import streamlit as st
import ydf
model_1 = ydf.load_model("buchwald_classifier_1")
model_2 = ydf.load_model("buchwald_classifier_2")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# test analyze function in script_interface.py

from green_chemistry.script_interface import analyze

def test_analyze():
    # Setup minimal working session_state to ensure analyze function is working well
    st.session_state["reagents"] = [{
        "MolecularWeight": "18.0",  # Water, for example
        "Title": "Water",
    }]
    st.session_state["product"] = [{
        "MolecularWeight": "36.0",  # Hypothetical product
        "Title": "Hydrogen Peroxide",
    }]
    st.session_state["solvents"] = []
    st.session_state["catalyzer"] = []
    st.session_state["temperature"] = 25
    st.session_state["pressure"] = 1

    result = analyze()

    assert result is not None, "Expected a result from analyze()"
    assert "atom_economy" in result
    assert "metal_analysis" in result
    assert "temperature_efficiency" in result
    assert "pressure_efficiency" in result
