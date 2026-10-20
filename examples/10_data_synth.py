import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from taskforge.data.synth import synthesize_goal
from taskforge.data.tasks import render_goal

sc = synthesize_goal("goal-0")
print("goal  :", render_goal("sales_report"))
print("subgoals:", sc.subgoals)
