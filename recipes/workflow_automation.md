# 配方：跨 SaaS 企业工作流自动化

目标：从「整理销售数据 → 发邮件给团队」这类自然语言，端到端跑完一条链。

```python
from taskforge.config import Config
from taskforge.engine import TaskforgeEngine

eng = TaskforgeEngine(Config())
eng.backend.skill = 1.0          # 换成真实后端即接入生产
res = eng.run("goal-0")
assert res.success
```

要点：子目标序列 + 工具链 + 动作接地三层分离，任何一层可单独替换。
