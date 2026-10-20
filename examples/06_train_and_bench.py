import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from taskforge.config import Config
from taskforge.model.backends import get_backend
from taskforge.train import train
from taskforge.bench.registry import run_all
import json

cfg = Config()
b = get_backend("mock", cfg)
print("skill before:", b.skill)
train(b)
print("skill after :", b.skill)

for name, r in run_all(cfg, b).items():
    print("%-12s %s" % (name, json.dumps(r, ensure_ascii=False)))
