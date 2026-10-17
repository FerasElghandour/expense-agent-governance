"""Offline example using the public implementation; see README for evidence scope."""
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
os.chdir(ROOT)

from policy import Claim,route,equal_split,monthly_cost
print({'at_threshold':route(Claim(50000,.9,True,True)),'over_threshold':route(Claim(50001,.9,True,True)),'allocation':equal_split(100,3),'monthly_cost':str(monthly_cost(1000,.02,.1,5,60,100))})
