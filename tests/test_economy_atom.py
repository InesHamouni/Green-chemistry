
import sys
import os 
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Test the atom_economy function 

from green_chemistry.atom_economy import atom_economy

def test_atom_economy():
    # Example: A + B → C
    # Molar mass of C (desired product): 100 g/mol
    # Molar mass of A: 50 g/mol
    # Molar mass of B: 70 g/mol
    economy, verdict = atom_economy(100, [50, 70])
    
    # Print the results (just for manual check if needed)
    print(f"Atom economy: {economy}%")
    print(f"Verdict: {verdict}")

    # Test expectations (just basic checks)
    assert isinstance(economy, float)
    assert isinstance(verdict, str)