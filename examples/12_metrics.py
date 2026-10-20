import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from taskforge.metrics.cost import estimate_cost
from taskforge.metrics.latency import estimate_latency

print("cost   :", round(estimate_cost(10000, 2000), 4), "CNY")
print("latency:", round(estimate_latency(200, 800), 3), "s")
