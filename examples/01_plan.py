import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from taskforge.config import Config
from taskforge.model.backends import get_backend
from taskforge.oracle import goal_subgoals, plan_correct

cfg = Config()
b = get_backend("mock", cfg)
b.skill = 1.0

for gid in ("goal-0", "goal-1", "goal-2"):
    plan = b.plan(gid)
    print("%s -> %s  correct=%s" % (gid, plan, plan_correct(gid, plan)))
