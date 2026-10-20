import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from taskforge.config import Config
from taskforge.model.backends import get_backend
from taskforge.planner.react import react_loop

cfg = Config()
b = get_backend("mock", cfg)
trace = react_loop(b, "goal-0", cfg.planner, observe=lambda a: {"ok": True})
print("react trace steps:", len(trace))
