import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from green_chemistry.pressure_efficiency import pressure_efficiency

print(pressure_efficiency(10))
