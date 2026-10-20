# 配方：电脑操作（GUI）自动化

```python
from taskforge.gui.agent import GuiAgent
from taskforge.model.backends import get_backend
from taskforge.config import Config

agent = GuiAgent(get_backend("mock", Config()))
rec = agent.act("scr-0", "intent-0")
```

要点：屏幕建模成「UI 元素树」而非原始像素，动作接地变成元素 id + 动作的离散选择。
