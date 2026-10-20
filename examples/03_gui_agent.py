import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from taskforge.config import Config
from taskforge.model.backends import get_backend
from taskforge.gui.agent import GuiAgent

cfg = Config()
b = get_backend("mock", cfg)
b.skill = 1.0
agent = GuiAgent(b)

for i in range(4):
    rec = agent.act("scr-%d" % i, "intent-%d" % i)
    print("screen=%s element=%s action=%s ok=%s" % (rec["screen"], rec["element"], rec["action"], rec["ok"]))
