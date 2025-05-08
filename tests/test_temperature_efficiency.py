import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from green_chemistry.temperature_efficiency import temperature_efficiency

print(temperature_efficiency(200))
