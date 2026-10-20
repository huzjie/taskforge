import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from taskforge.config import Config
from taskforge.engine import TaskforgeEngine

cfg = Config()
eng = TaskforgeEngine(cfg)
eng.backend.skill = 1.0

res = eng.run("goal-0")
print("goal   :", res.goal_id)
print("plan   :", res.plan)
print("success:", res.success)
print("steps  :", len(res.steps))
print("tokens :", res.tokens_used)
