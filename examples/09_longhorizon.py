import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from taskforge.config import Config
from taskforge.model.backends import get_backend
from taskforge.bench.longhorizon import run
import json

cfg = Config()
b = get_backend("mock", cfg)

for skill in (0.5, 0.75, 1.0):
    b.skill = skill
    r = run(cfg, b)
    print("skill=%.2f  %s" % (skill, json.dumps(r, ensure_ascii=False)))
