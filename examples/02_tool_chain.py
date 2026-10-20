import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from taskforge.config import Config
from taskforge.model.backends import get_backend
from taskforge.tools.orchestrator import ToolOrchestrator

cfg = Config()
b = get_backend("mock", cfg)
b.skill = 1.0
orch = ToolOrchestrator(b, cfg.tools)

for subgoal in ("search", "open", "extract", "submit"):
    step = orch.execute(subgoal)
    print("%-8s -> tool=%-14s ok=%s" % (subgoal, step["tool"], step["ok"]))
