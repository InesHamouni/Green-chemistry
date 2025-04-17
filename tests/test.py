
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Test the atom_economy function 

from green_chemistry.atom_economy import atom_economy

# Example: A + B → C
# Molar mass of C (desired product): 100 g/mol
# Molar mass of A: 50 g/mol
# Molar mass of B: 70 g/mol

economy, verdict = atom_economy(100, [50, 70])

# Output the results
print(f"Atom economy: {economy}%")
print(f"Verdict: {verdict}")
