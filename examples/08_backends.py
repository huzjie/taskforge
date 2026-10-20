import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from taskforge.config import Config
from taskforge.model.backends import list_backends, get_backend

print("registered backends:", list_backends())
for name in list_backends():
    b = get_backend(name, Config())
    print("  %-14s plan(goal-0) -> %s" % (name, b.plan("goal-0")))
