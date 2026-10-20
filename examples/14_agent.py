import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from taskforge.agent.loop import Agent

a = Agent()
a.engine.backend.skill = 1.0
out = a.run("goal-0")
print(out)
