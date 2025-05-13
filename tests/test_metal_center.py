import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from green_chemistry.metal_center import get_metal_impact

print(get_metal_impact("Pt"))